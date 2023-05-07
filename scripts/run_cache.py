import importlib.util
import os
import time
from datetime import datetime
from functools import partial
from typing import Dict, Optional

global_st = time.time()
if importlib.util.find_spec("src") is None:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import dask.dataframe as dd
from dotenv import load_dotenv
from sqlalchemy import create_engine

if load_dotenv():
    print(".env loaded")

from src.process_queue import TABLE_NAME_MAPPER
from src.constant import Chain
from src.erc20 import Token
from src.utils import print_log


# ROOT_DIR = "/home/ubuntu"
ROOT_DIR = "/Users/chompk.visai/Works/cdao/connext/connext-liquidity-dashboard"
MIN_VALUE = 1e-7
LATEST_DATE = None

CHAINS = [
    Chain.ARBITRUM_ONE,
    Chain.POLYGON,
    Chain.OPTIMISM,
    Chain.BNB_CHAIN,
    Chain.GNOSIS
]

CAMPAIGNS = {
    # https://galxe.com/connextnetwork/campaign/GC1SiU4gvJ
    "campaign_1": {
        "tokens": [Token.CUSDCLP, Token.CWETHLP],
        # 15 Feb 2023 00:00:00 UTC
        "start": datetime.fromtimestamp(1676419200),
        # 15 May 2023 00:00:00 UTC
        "end": datetime.fromtimestamp(1684108800),
    },
    # https://galxe.com/connextnetwork/campaign/GCEtNUya7s
    "campaign_2-rare": {
        "tokens": [Token.CUSDCLP, Token.CWETHLP],
        "start": None,
        "end": None,
    },
    "campaign_2": {
        "tokens": [Token.CUSDTLP, Token.CDAILP],
        "start": None,
        "end": None,
    }
}


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


def get_checkpoint_dates(campaign_name: str) -> Optional[Dict[str, datetime]]:
    """Get checkpoint dates for a campaign
    """
    checkpoint_dates = {}
    campaign = CAMPAIGNS.get(campaign_name, None)

    if campaign is None:
        print_log(f"Campaign {campaign_name} not found")
        return None

    if campaign["start"] is None or campaign["end"] is None:
        # campaign has not started or ended
        print_log(f"Campaign {campaign_name} has not started or ended")
        return None

    if LATEST_DATE > campaign["end"]:
        # campaign has ended
        print_log(f"Campaign {campaign_name} has ended, using end date as checkpoint")
        checkpoint_dates["end"] = campaign["end"]
    else:
        # campaign is still running
        print_log(f"Campaign {campaign_name} is still running, using latest date as checkpoint")
        checkpoint_dates["end"] = LATEST_DATE

    if LATEST_DATE > campaign["start"]:
        # campaign has started
        checkpoint_dates["start"] = campaign["start"]
    else:
        # campaign has not started
        print_log(f"Campaign {campaign_name} has not started, skipping...")
        return None
    return checkpoint_dates


def calculate_average_balance_by_minute(
    user_balance: pd.Series,
    start_time: datetime,
    end_time: datetime,
) -> float:
    """
    Calculate average user balance by minute
    """
    temp = pd.Series(data=[0., 0.], index=[start_time, end_time], name="balance_change")
    score = pd.concat(
        [user_balance, temp]
    ).sort_index().cumsum().resample("T").last().ffill().between_time(
        start_time.time(), 
        end_time.time()).mean()

    return score


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
            print_log(f"processing {campaign_name}...")
            checkpoint_dates = get_checkpoint_dates(campaign_name)
            if checkpoint_dates is None:
                print_log(f"no checkpoint dates for {campaign_name}, skipping...")
                continue
            print_log(f"Campaign checkpoint dates: {checkpoint_dates['start']} - {checkpoint_dates['end']}")

            # compute user scores of each campaign
            st = time.time()
            dataset = dd.from_pandas(dataset[dataset["token"].isin(campaign["tokens"])], npartitions=5)
            user_scores = dataset.groupby(["user_address", "token"])["balance_change"].apply(
                partial(
                    calculate_average_balance_by_minute, 
                    start_time=checkpoint_dates["start"],
                    end_time=checkpoint_dates["end"],
                ),
                meta=("balance_change", float)
            ).compute()
            print_log(f"compute user scores: {time.time() - st:.2f} seconds")

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
