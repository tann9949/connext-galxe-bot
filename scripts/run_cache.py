import os
import time
global_st = time.time()
from datetime import datetime

import pandas as pd
import dask.dataframe as dd
from dotenv import load_dotenv
from sqlalchemy import create_engine

if load_dotenv():
    print(".env loaded")

from src.process_queue import TABLE_NAME_MAPPER
from src.constant import Chain
from src.token import Token
from src.utils import print_log


CHAINS = [
    Chain.ARBITRUM_ONE,
    Chain.POLYGON,
    Chain.OPTIMISM,
    Chain.BNB_CHAIN,
    Chain.GNOSIS
]

CAMPAIGN_START_DATETIME = datetime.fromtimestamp(1676419200)
ROOT_DIR = "/home/ubuntu"
MIN_VALUE = 1e-7
LATEST_DATE = None


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


def calculate_average_balance_by_minute(user_balance):
    temp = pd.Series(data=[0., 0.], index=[CAMPAIGN_START_DATETIME, LATEST_DATE], name="balance_change")
    score = pd.concat(
        [user_balance, temp]
    ).sort_index().cumsum().resample("T").last().ffill().between_time(
        CAMPAIGN_START_DATETIME.time(), 
        LATEST_DATE.time()).mean()

    return score


def main() -> None:
    print_log(f"process started in {time.time() - global_st:.2f} seconds")

    all_chains_data = []
    for chain in CHAINS:
        print_log(f"loading dataset for {Chain.resolve_connext_domain(chain)}...")
        st = time.time()
        dataset = load_dataset(chain)
        all_chains_data.append(dataset)
        global LATEST_DATE
        LATEST_DATE = dataset.index.max()

        dataset = dd.from_pandas(dataset, npartitions=5)
        print_log(f"{len(dataset)} data loaded")
        print_log(f"dataset loaded in {time.time() - st:.2f} seconds")

        st = time.time()
        user_scores = dataset.groupby(["user_address", "token"])["balance_change"].apply(
            calculate_average_balance_by_minute, 
            meta=("balance_change", float)
        ).compute()
        print_log(f"compute user scores: {time.time() - st:.2f} seconds")

        st = time.time()
        save_cache(
            user_scores, 
            f"{ROOT_DIR}/cache/{Chain.resolve_connext_domain(chain)}_user_scores.csv")
        print_log(f"cache user scores: {time.time() - st:.2f} seconds")
        print_log(f"cache for {Chain.resolve_connext_domain(chain)} completed")

    all_chains_data = pd.concat(all_chains_data, axis=0).to_csv(f"{ROOT_DIR}/cache/full_dataset.csv")

    print_log(f"total time: {time.time() - global_st:.2f} seconds")


if __name__ == "__main__":
    main()
