import importlib.util
import os
import time
from datetime import datetime
from functools import partial


global_st = time.time()
if importlib.util.find_spec("src") is None:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dask.dataframe as dd
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

if load_dotenv():
    print(".env loaded")

from src.campaign import CAMPAIGNS, get_checkpoint_dates
from src.constant import Chain
from src.erc20 import Token
from src.process_queue import TABLE_NAME_MAPPER
from src.utils import print_log

ROOT_DIR = os.getenv("ROOT_DIR", "/home/ubuntu")
MIN_VALUE = 1e-7
LATEST_DATE = None

CHAINS = [
    Chain.ARBITRUM_ONE,
    Chain.POLYGON,
    Chain.OPTIMISM,
    Chain.BNB_CHAIN,
    Chain.GNOSIS
]


def resolve_action(action: int) -> str:
    action = int(action)
    if action == 1:
        return "mint"
    elif action == 2:
        return "burn"
    elif action == 3:
        return "transfer_in"
    elif action == 4:
        return "transfer_out"


def load_dataset(chain: Chain):
    cnx = create_engine(
        f"mysql+pymysql://{os.getenv('AWS_RDS_USERNAME')}:{os.getenv('AWS_RDS_PASSWORD')}@{os.getenv('AWS_RDS_HOSTNAME')}/connext")
            
    dataset = []
    table_name = TABLE_NAME_MAPPER.get(chain)
    df = pd.read_sql(
        f"SELECT * FROM {table_name}",
        cnx
    )
    df["datetime"] = df["timestamp"].copy().map(datetime.fromtimestamp)
    df["action"] = df["action"].copy().map(resolve_action)
    df["chain"] = df["chain"].copy().map(Chain.resolve_connext_domain)
    df["token"] = df["token_address"].map(
        lambda x: Token.address_lookup(x, chain=chain).symbol
    )
    df = df.drop([
        "id",
        "timestamp",
    ], axis=1).drop_duplicates()
    df = df[
        ["datetime", "chain", "hash", "user_address", "token", "token_amount", "action"]
    ]
    dataset.append(df)
    dataset = pd.concat(dataset, axis=0)
    dataset = dataset.set_index("datetime").sort_index()
    dataset["balance_change"] = dataset["token_amount"].copy() \
        * dataset["action"].copy().map(
            lambda x: 1 if x in ["mint", "transfer_in"] else -1
    )
    return dataset


def save_cache(df: pd.DataFrame, filename: str):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df.to_csv(filename)


def calculate_average_balance_by_minute(
    user_balance: pd.Series,
    start_time: datetime,
    end_time: datetime,
) -> float:
    """
    Calculate average user balance by minute
    """
    temp = pd.Series(data=[0., 0.], index=[start_time, end_time], name="balance_change")
    resampled_score = pd.concat(
        [user_balance, temp]
    ).sort_index().cumsum().resample("T").last().ffill()[start_time:end_time]
    score = resampled_score.mean()
    minutes_qualified = int((resampled_score.apply(
        lambda x: 0 if x < MIN_VALUE else x
    ) > 0).sum())
    del resampled_score

    return score, minutes_qualified


def main() -> None:
    print_log(f"process started in {time.time() - global_st:.2f} seconds")

    all_chains_data = []
    for chain in CHAINS:
        # Load dataset from RDS
        print_log(f"loading dataset for {Chain.resolve_connext_domain(chain)}...")
        st = time.time()
        dataset = load_dataset(chain)
        all_chains_data.append(dataset)
        # get latest date from each chaind database
        global LATEST_DATE
        LATEST_DATE = dataset.index.max()

        print_log(f"{len(dataset)} data loaded")
        print_log(f"dataset loaded in {time.time() - st:.2f} seconds")

        for campaign_name, campaign in CAMPAIGNS.items():
            # if campaign already ended, skip
            if campaign["end"] < datetime.now():
                print_log(f"{campaign_name} already ended, skip caching...")
                continue

            print_log(f"processing {campaign_name}...")
            checkpoint_dates = get_checkpoint_dates(
                campaign_name=campaign_name, 
                latest_date=LATEST_DATE)
            if checkpoint_dates is None:
                print_log(f"no checkpoint dates for {campaign_name}, skipping...")
                continue
            print_log(f"Campaign checkpoint dates: {checkpoint_dates['start']} - {checkpoint_dates['end']}")

            # compute user scores of each campaign
            st = time.time()
            dask_dataset = dd.from_pandas(dataset[dataset["token"].isin(campaign["tokens"])], npartitions=5)

            groupby_list = ["user_address", "token"]

            user_scores = dask_dataset.groupby(groupby_list)["balance_change"].apply(
                partial(
                    calculate_average_balance_by_minute, 
                    start_time=checkpoint_dates["start"],
                    end_time=checkpoint_dates["end"],
                ),
                meta=("balance_change", float)
            ).compute()
            print_log(f"compute user scores: {time.time() - st:.2f} seconds")

            user_scores = pd.DataFrame(user_scores.tolist(), index=user_scores.index, columns=["score", "minutes_qualified"])

            st = time.time()
            save_cache(
                user_scores, 
                f"{ROOT_DIR}/cache/{campaign_name}/{Chain.resolve_connext_domain(chain)}_user_scores.csv")
            print_log(f"cache user scores: {time.time() - st:.2f} seconds")
            print_log(f"cache for {Chain.resolve_connext_domain(chain)} completed")

    all_chains_data = pd.concat(all_chains_data, axis=0).to_csv(f"{ROOT_DIR}/cache/full_dataset.csv")

    print_log(f"total time: {time.time() - global_st:.2f} seconds")


if __name__ == "__main__":
    main()
