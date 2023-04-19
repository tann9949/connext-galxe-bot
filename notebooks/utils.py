import os
import sys
from datetime import datetime
from typing import Any, Dict, List
if os.path.join(os.getcwd(), "..") not in sys.path:
    sys.path.append(os.path.join(os.getcwd(), ".."))

import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

from src.constant import Chain
from src.process_queue import TABLE_NAME_MAPPER
from src.token import Token
from src.utils import print_log

CAMPAIGN_START_DATETIME = datetime.strptime("2023-02-15", "%Y-%m-%d")


class Utility:
    @staticmethod
    def resolve_action(action: int) -> str:
        if action == 1:
            return "mint"
        elif action == 2:
            return "burn"
        elif action == 3:
            return "transfer_in"
        elif action == 4:
            return "transfer_out"
        
    @staticmethod
    def get_days_from_second(seconds: float) -> float:
        minutes = seconds / 60
        hours = minutes / 60
        return hours / 24
    
class CacheUtils:
    
    @staticmethod
    def save_cache(
        chain: Chain, 
        cache_path: str = "cache", 
        reload: bool = True
    ) -> None:
        os.makedirs(cache_path, exist_ok=True)
        cache_path = os.path.join(
            cache_path, 
            Chain.resolve_connext_domain(chain)
        ) + ".csv"
        if os.path.exists(cache_path) and not reload:
            print_log("Cache already existed!")
            return
        else:
            print_log("Reloading data...")

        table_name = TABLE_NAME_MAPPER.get(chain)
        cnx = create_engine(
            f"mysql+pymysql://{os.getenv('AWS_RDS_USERNAME')}:{os.getenv('AWS_RDS_PASSWORD')}@{os.getenv('AWS_RDS_HOSTNAME')}/connext")
        df = pd.read_sql(
            f"SELECT * FROM {table_name}",
            cnx
        )
        df.to_csv(cache_path, index=False)
        print_log("Cache saved successfully!")
        
        
class DataUtils:
    
    @staticmethod
    def load_txn_data(
        chain: Chain, 
        use_cache: bool = True, 
        cache_path: str = "cache"
    ) -> pd.DataFrame:
        cache_path = os.path.join(cache_path, Chain.resolve_connext_domain(chain)) + ".csv"
        if use_cache and os.path.exists(cache_path):
            print_log("Cache loaded successfully!")
            df = pd.read_csv(cache_path)
        else:
            print_log("Cache not found, loading from AWS RDS")
            table_name = TABLE_NAME_MAPPER.get(chain)
            cnx = create_engine(
                f"mysql+pymysql://{os.getenv('AWS_RDS_USERNAME')}:{os.getenv('AWS_RDS_PASSWORD')}@{os.getenv('AWS_RDS_HOSTNAME')}/connext")
            df = pd.read_sql(
                f"SELECT * FROM {table_name}",
                cnx
            )
        df["datetime"] = df["timestamp"].copy().map(datetime.fromtimestamp)
        df["action"] = df["action"].copy().map(Utility.resolve_action)
        df["chain"] = df["chain"].copy().map(Chain.resolve_connext_domain)
        df["token"] = df["token_address"].map(
            lambda x: Token.address_lookup(x, chain=chain).symbol
        )
        df = df.drop([
            "id",
            "timestamp",
        ], axis=1).drop_duplicates()
        return df[
            ["datetime", "chain", "hash", "user_address", "token", "token_amount", "action"]
        ]
    
    @staticmethod
    def load_dataset(chains: List[Chain]) -> Dict[Chain, pd.DataFrame]:
        dataset = {}
        for chain in chains:
            df = DataUtils.load_txn_data(chain)
            print_log(f"Data loaded from chain {Chain.resolve_connext_domain(chain)}, total of {len(df)} record")
            dataset[chain] = df
        return dataset
        
    
    
class ProcessingUtils:
    
    @staticmethod
    def get_lp_holdings_day(
        user_balance: pd.Series,
        latest_date: datetime,
        min_value: float = 1e-4,
    ) -> int:
        total_seconds = 0

        init_balance = user_balance.iloc[0]
        running_start = user_balance.index[0]
        for i in range(len(user_balance)-1):
            curr, nxt = user_balance.iloc[i], user_balance.iloc[i+1]
            if curr == 0 and nxt > 0:
                # add liquidity
                running_start = user_balance.index[i+1]
            elif curr > 0 and nxt == 0:
                # remove liquidity
                duration = user_balance.index[i+1] - running_start
                total_seconds += duration.total_seconds()
                running_start = None
        if running_start:
            total_seconds = (latest_date - running_start).total_seconds()
        return Utility.get_days_from_second(total_seconds)
    
    @staticmethod
    def get_user_txs(
        dataset: Dict[Chain, pd.DataFrame],
        chain: Chain, 
        latest_date: datetime,
        min_lp_value: float = 1e-4, 
    ) -> Dict[str, Dict[str, pd.DataFrame]]:
        """
        Get per-user transaction infos

        Arguments:
        chain: Chain
            - A chain specified to analyze the data
        min_lp_value: float
            - Minimum of LP holdings to consider as holding
        timeframe: str
            - Timeframe to average
        """
        df = dataset[chain].copy()
        df = df[df["token"].isin([Token.CUSDCLP, Token.CWETHLP])]
        df["balance_change"] = df["action"].isin(
            ["mint", "transfer_in"]
        ).map(lambda x: 1 if x else -1) * df["token_amount"]

        user_txs = dict()
        for _user in tqdm(
            df["user_address"].unique(),
            desc=f"Analyzing users in {Chain.resolve_connext_domain(chain).capitalize()}"):
            for token in [Token.CWETHLP, Token.CUSDCLP]:

                user_tx = df[
                    (df["user_address"] == _user) & \
                    (df["token"] == token)
                ].set_index("datetime").drop(["chain", "token"], axis=1)

                # we won't count as user if 
                # there's no tx for those user
                if len(user_tx) == 0:
                    continue

                # add null transaction at start camapaign
                # and the latest date
                user_tx = pd.concat([user_tx, pd.DataFrame([{
                    "hash": "",
                    "user_address": _user,
                    "token_amount": 0,
                    "action": "",
                    "balance_change": 0
                }, {
                    "hash": "",
                    "user_address": _user,
                    "token_amount": 0,
                    "action": "",
                    "balance_change": 0
                }], index=[CAMPAIGN_START_DATETIME, latest_date])], axis=0)
                user_tx = user_tx.sort_index()

                # skip if final balance is less than minimum value
                user_balance = user_tx["balance_change"].cumsum()
                if len(user_balance) <= 2 and user_balance.values[-1] < min_lp_value:
                    continue

                # add data to dictionary
                if _user not in user_txs:
                    user_txs[_user] = {}
                user_txs[_user][token] = user_tx

        return user_txs


    def process_user_balance(
        user_tx: pd.DataFrame, 
        latest_date: datetime,
        timeframe: str = "1T",
        min_lp_value: float = 1e-4
    ) -> Dict[str, Any]:
        # cumulative sum balance change to get balance
        user_balance = user_tx["balance_change"].cumsum()
        # fix any decimal point error
        user_balance = user_balance[user_balance.index >= CAMPAIGN_START_DATETIME].clip(lower=0)
        # calculate active lp holding days
        elapsed_days = ProcessingUtils.get_lp_holdings_day(user_balance, min_value=min_lp_value, latest_date=latest_date)
        # resample to specific timeframe
        resampled_balance = user_balance.resample(timeframe).last().ffill()
        # calculate time-weighted average LP holdings
        twa_balance = resampled_balance.mean()

        return {
            "elapsed_days": elapsed_days,
            "resampled_balance": resampled_balance,
            "twa_balance": twa_balance
        }

    
class VisualizeUtils:
    
    @staticmethod
    def visualize_lps(dataset: Dict[Chain, pd.DataFrame], chain: Chain) -> None:
        df = dataset[chain]

        fig, ax = plt.subplots(2, 2, figsize=(30, 20))
        for i, token in enumerate([Token.CUSDCLP, Token.CWETHLP]):
            token_txn = df[df["token"] == token]
            mint_txn = token_txn[token_txn["action"] == "mint"]
            burn_txn = token_txn[token_txn["action"] == "burn"]

            mint_txn[mint_txn["datetime"] >= CAMPAIGN_START_DATETIME]\
                .set_index("datetime").resample("1H").count()["action"].cumsum().ffill().plot(label="# mint transaction", ax=ax[i][0])
            burn_txn[burn_txn["datetime"] >= CAMPAIGN_START_DATETIME]\
                .set_index("datetime").resample("1H").count()["action"].cumsum().ffill().plot(label="# burn transaction", ax=ax[i][0])

            ax[i][0].axvline(
                datetime.strptime("2023-03-11", "%Y-%m-%d"),
                linestyle="--",
                alpha=0.3,
                color="black",
                label="USDC Depeg Incident"
            )
            ax[i][0].set_ylabel("Number of transactions")
            ax[i][0].set_title(f"Number of transactions of mint/burn for {token} at {Chain.resolve_connext_domain(chain).capitalize()}")
            ax[i][0].legend()


            (
                mint_txn[mint_txn["datetime"] >= datetime.strptime("2023-02-15", "%Y-%m-%d")]\
                    .set_index("datetime").resample("1H")["token_amount"].sum().cumsum() - \
                burn_txn[burn_txn["datetime"] >= datetime.strptime("2023-02-15", "%Y-%m-%d")]\
                    .set_index("datetime").resample("1H")["token_amount"].sum().cumsum()
            ).ffill().plot(ax=ax[i][1])
            
            ax[i][1].axvline(
                datetime.strptime("2023-03-11", "%Y-%m-%d"),
                linestyle="--",
                alpha=0.3,
                color="black",
                label="USDC Depeg Incident"
            )
            ax[i][1].set_ylabel("CUSDCLP TVL (in million)")
            ax[i][1].set_title(f"TVL of {token} at {Chain.resolve_connext_domain(chain).capitalize()}")

        plt.legend()
        plt.tight_layout()
        plt.show()