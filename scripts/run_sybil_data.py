import importlib.util
import os
import time
from argparse import ArgumentParser, Namespace
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Tuple

global_st = time.time()
if importlib.util.find_spec("src") is None:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

if load_dotenv():
    print(".env loaded")

from src.campaign import CAMPAIGNS, get_checkpoint_dates
from src.constant import Chain
from src.contract import SmartContract
from src.erc20 import Token
from src.process_queue import TABLE_NAME_MAPPER
from src.scan import ScanAPI, ScanTxn
from src.utils import print_log

CHAINS = [
    Chain.ARBITRUM_ONE,
    Chain.BNB_CHAIN,
    Chain.GNOSIS,
    Chain.OPTIMISM,
    Chain.POLYGON
]

class Campaign:
    CAMPAIGN_1 = "campaign_1"
    CAMPAIGN_2 = "campaign_2"


def run_parser() -> Namespace:
    parser = ArgumentParser(
        description="Fetch historical USDC, WETH, or ETH transfers during a specific campaign, and store it on the database",
        epilog="Example: python run_sybil_data.py --campaign=campaign_1",
    )
    parser.add_argument(
        "--campaign",
        type=str,
        required=True,
        choices=[Campaign.CAMPAIGN_1, Campaign.CAMPAIGN_2],
        help="Campaign to run on (campaign_1, campaign_2)",
    )
    return parser.parse_args()


def load_dataset(chain: Chain) -> pd.DataFrame:
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


def get_campaign1_participants(
    min_usdc: float = 1e-7, 
    min_weth: float = 1e-7,
    minimum_days: int = 30
) -> Dict[str, List[str]]:
    """Get eligible users for the campaign filtered by 30 days criteria"""
    campaign = CAMPAIGNS.get("campaign_1")
    campaign_lp_tokens: List[Token] = campaign.get("tokens", [])
    minimum_position_minutes = timedelta(days=minimum_days).total_seconds() // 60
    
    participants = {Chain.resolve_connext_domain(chain): {} for chain in CHAINS}
    # get unique participants from each chain+pool with minimum of 30 days provided
    for chain in CHAINS:
        chain_data = load_dataset(chain)
        chain = Chain.resolve_connext_domain(chain)
        for _token in campaign_lp_tokens:
            print(f"Computing eligible users for {chain}, {_token} pool")
            # adjust this accordingly
            min_token_value = min_usdc if _token == Token.CWETHLP else min_weth
            token_positions = chain_data[chain_data["token"] == _token]
            holdings_minutes = token_positions.groupby(["user_address", "token"]).apply(
                lambda positions: ((
                    pd.concat(
                        [
                            positions["balance_change"], 
                            pd.Series(
                                data=[0., 0.], 
                                index=[
                                    campaign["start"], 
                                    campaign["end"]
                                ], 
                                name="balance_change")
                        ]
                    )\
                    .sort_index()\
                    .cumsum()\
                    .resample("T")\
                    .last()\
                    .ffill()\
                    [campaign["start"]:campaign["end"]]
                ) > min_token_value).sum()
            )
            eligible_users = holdings_minutes[holdings_minutes > minimum_position_minutes]
            participants[chain][_token] = sorted(set([_addr for _addr, _ in eligible_users.index]))
    
    # group each chain into 3 category: USDC only, WETH only, and both
    grouped_participants = {Chain.resolve_connext_domain(chain): {} for chain in CHAINS}
    for chain in CHAINS:
        chain = Chain.resolve_connext_domain(chain)
        usdc_participants = participants[chain][Token.CUSDCLP]
        weth_participants = participants[chain][Token.CWETHLP]
        # get participants that qualified for both
        both_participants = list(set(usdc_participants).intersection(set(weth_participants)))
        # isolate single pool provider
        usdc_participants = list(set(usdc_participants) - set(both_participants))
        weth_participants = list(set(weth_participants) - set(both_participants))
        grouped_participants[chain] = {
            Token.USDC: usdc_participants,
            Token.WETH: weth_participants,
            "both": both_participants
        }

    return grouped_participants


def is_account(address: str, chain: Chain) -> bool:
    provider = SmartContract.get_default_provider(chain)
    if address.lower() == address:
        address = provider.to_checksum_address(address)
    code = provider.eth.get_code(address).hex()
    if code == "0x":
        return True
    return False


def get_transfers_to_acc(
    user_address: str, 
    token_address: str, 
    chain: Chain, 
    campaign_name: Campaign,
    cache_dir: str = None
) -> Optional[Tuple[List[ScanTxn], List[ScanTxn]]]:
    scan_api = ScanAPI(chain, apikey_schedule="random")
    campaign = CAMPAIGNS.get(campaign_name)
    transfer_txs = scan_api.get_transfer_events(
        token_address=token_address, 
        address=user_address, startblock=scan_api.get_block_by_datetime(campaign["start"]), 
        endblock=scan_api.get_block_by_datetime(campaign["end"]))

    # filter to get only transfer out events
    account_transfer_txs = []
    smart_contract_transfer_txs = []
    for _tx in transfer_txs:
        if _tx.from_address == user_address.lower():
            # skip receive transactions
            continue
        if is_account(_tx.to_address, chain):
            account_transfer_txs.append(_tx)
        else:
            smart_contract_transfer_txs.append(_tx)

    if cache_dir is None:
        return account_transfer_txs, smart_contract_transfer_txs
    else:
        # store cache
        token_name = Token.address_lookup(token_address, chain).symbol
        cache_path = f"{cache_dir}/sybil/{campaign_name}/{chain}/{token_name}/{user_address}.json"
        print("cache_path", cache_path)


def main(args: Namespace) -> None:
    cache_dir = "./cache"
    campaign_name = args.campaign
    campaign: Dict[str, Union[List[Token], datetime]] = CAMPAIGNS.get(campaign_name)

    if campaign_name == Campaign.CAMPAIGN_1:
        eligible_users = get_campaign1_participants()
    else:
        raise NameError(f"Campaign is not supported yet")
    
    # predefined jobs
    canonical_jobs = []
    next_jobs = []
    for chain in CHAINS:
        domain_id = chain
        chain = Chain.resolve_connext_domain(chain)
        for token in eligible_users[chain]:
            if token == "both":
                tokens = [_token for _token in eligible_users[chain] if _token != "both"]
            else:
                tokens = [token]

            for _acc in eligible_users[chain][token]:
                for _token in tokens:
                    canonical_addr = Token.get_canonical(
                        domain_id, 
                        _token).address
                    next_addr = Token.get_next(
                        domain_id, 
                        _token).address
                    
                    canonical_jobs.append({
                        "user_address": _acc,
                        "token_address": canonical_addr,
                        "chain": domain_id,
                        "campaign_name": campaign_name,
                        "cache_dir": cache_dir
                    })
                    next_jobs.append({
                        "user_address": _acc,
                        "token_address": next_addr,
                        "chain": domain_id,
                        "campaign_name": campaign_name,
                        "cache_dir": cache_dir
                    })

    print(f"Total {len(canonical_jobs)+len(next_jobs)} needed to be computed")
    get_transfers_to_acc(**canonical_jobs[0])




if __name__ == "__main__":
    args = run_parser()
    main(args)
