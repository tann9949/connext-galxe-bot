import os
from datetime import datetime

import pymysql

from .utils import print_log
from .constant import Action, Chain, DiamondContract
from .scan import ScanAPI
from .token import Token
from .topic_resolver import get_topic_resolver


TABLE_NAME_MAPPER = {
    Chain.POLYGON: "PolygonTransactions",
    Chain.ARBITRUM_ONE: "ArbitrumTransactions",
    Chain.GNOSIS: "GnosisTransactions",
    Chain.BNB_CHAIN: "BNBChainTransactions",
    Chain.OPTIMISM: "OptimismTransactions",
}

# worker parameters
CHAINS = [
    # Chain.ETHEREUM,  # ignore this chain, no AMM
    Chain.POLYGON, 
    Chain.ARBITRUM_ONE, 
    Chain.GNOSIS, 
    Chain.BNB_CHAIN, 
    Chain.OPTIMISM
]
FUNCTIONS = [
    "addSwapLiquidity", 
    "removeSwapLiquidity"
]
TOPICS = [ "Transfer" ]
CONNEXT_TOKENS = list(map(str.lower, [
    "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",
    "0x2170Ed0880ac9A755fd29B2688956BD959F933F8",
    "0x5e7D83dA751F4C9694b13aF351B30aC108f32C38",
    "0xA9CB51C666D2AF451d87442Be50747B31BB7d805",
    "0xc170908481E928DfA39DE3D0d31bEa6292692F8e",
    "0x223F6A3B8d087741BF99a2531DC53cd15745eBa7",
    "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
    "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
    "0xF96C6d2537e1af1a9503852eB2A4AF264272a5B6",
    "0x4b8BaC8Dd1CAA52E32C07755c17eFadeD6A0bbD0",
    "0xa03258b76Ef13AF716370529358f6A79eb03ec12",
    "0xeF1348dAC70e8349513E4Ae7498F302e27102101",
    "0x7F5c764cBc14f9669B88837ca1490cCa17c31607",
    "0x4200000000000000000000000000000000000006",
    "0x67E51f46e8e14D4E4cab9dF48c59ad8F512486DD",
    "0xbAD5B3c68F855EaEcE68203312Fd88AD3D365e50",
    "0xB12A1Be740B99D845Af98098965af761be6BD7fE",
    "0x3C12765d3cFaC132dE161BC6083C886B2Cd94934",
    "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8",
    "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
    "0x8c556cF37faa0eeDAC7aE665f1Bb0FbD4b2eae36",
    "0x2983bf5c334743Aa6657AD70A55041d720d225dB",
    "0xDa492C29D88FfE9B7cbfA6DC068C2f9befaE851b",
    "0xb86AF5eB59A8e871bfA573FA656123ea86F47c3a",
    "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83",
    "0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1",
    "0x44CF74238d840a5fEBB0eAa089D05b763B73faB8",
    "0x538E2dDbfDf476D24cCb1477A518A82C9EA81326",
    "0xA639FB3f8C52e10E10a8623616484d41765d5F82",
    "0x7aC5bBefAE0459F007891f9Bd245F6beaa91076c",
]))

# constant to resolve topic id
TOPIC2SIG = get_topic_resolver()


def resolve_address(address: str) -> str:
    """ensure padding to length of 40 (excluded 0x)"""
    hex_code = address.replace("0x", "")
    if len(hex_code) < 40:
        n_zeros = 40 - len(hex_code)
        hex_code = "0" * n_zeros + hex_code
    resolved_address = "0x" + hex_code
    assert len(resolved_address) == 42
    return resolved_address


def get_block_range(chain: Chain, start_datetime: str, end_datetime: str) -> tuple:
    """
    Get block range from datetime
    """
    scan_api = ScanAPI(chain, apikey_schedule="random")
    start_datetime = datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M:%S")
    end_datetime = datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M:%S")
    start_block = scan_api.get_block_by_datetime(start_datetime, close="before")
    end_block = scan_api.get_block_by_datetime(end_datetime, close="after")
    return start_block, end_block


def insert_transactions(
    fetched_items: list, 
    table_name: str,
) -> None:
    print(f"Adding {len(fetched_items)} items to mysql db")
    cnx = pymysql.connect(
        host=os.getenv("AWS_RDS_HOSTNAME"),
        user=os.getenv("AWS_RDS_USERNAME"),
        password=os.getenv("AWS_RDS_PASSWORD"),
        database="connext"
    )
    # add to mysql db
    for item in fetched_items:
        with cnx.cursor() as cursor:
            print_log(f"Adding {item} to mysql db")
            query = (
                f"INSERT INTO {table_name} "
                "(timestamp, chain, hash, user_address, token_address, token_amount, action) "
                "VALUES (%(timestamp)s, %(chain)s, %(hash)s, %(user_address)s, %(token_address)s, %(token_amount)s, %(action)s)"
            )
            cursor.execute(query, item)
            cnx.commit()
            print_log(cursor.rowcount, "record inserted.")


def process_transaction(
    record: dict, 
) -> list:
    """
    Process a transaction record from AWS SQS
    """
    chain = int(record.get("chain"))
    table_name = TABLE_NAME_MAPPER.get(chain)
    start_datetime = record.get("start_datetime")
    end_datetime = record.get("end_datetime")
    if not chain:
        raise Exception("Chain not found in queue record")
    scan_api = ScanAPI(chain, apikey_schedule="random")
    
    start_block, end_block = get_block_range(chain, start_datetime, end_datetime)
    txs = scan_api.get_transaction_by_address(
        DiamondContract.get_contract_address(chain),
        startblock=start_block,
        endblock=end_block,
    )

    fetched_items = []
    # iterate over all transactions
    for tx in txs:
        try:
            # filter non-liquidity txs
            tx_error = bool(tx.isError)
            tx_function = tx.functionName.split("(")[0]
            if tx_error or tx_function not in FUNCTIONS:
                print_log(f"Skipping {tx_function} transaction {tx.hash}")
                continue

            # skip if transaction already have receipt
            if tx.logs is not None:
                continue

            # resolve tx receipt
            print_log(f"Resolving transaction {tx.hash}")
            receipt = scan_api.get_transaction_receipt(
                tx.hash, max_attempt=10, wait_time=1)
            
            # skip if receipt is not available
            if isinstance(receipt, str):
                print_log(f"Error: {receipt}")
                continue

            # iterate over all logs
            logs = receipt["logs"]
            for _log in logs:
                # resolve topic
                topic, *topic_args = _log["topics"]
                topic_items = TOPIC2SIG.get(topic)

                # skip unknown topic name
                if topic_items is None: 
                    continue
                topic_name, *topic_params = topic_items

                # filter unwanted topic
                if topic_name not in TOPICS:
                    print_log(f"Skipping {topic_name} topic")
                    continue

                # skip unwanted address
                if _log["address"].lower() not in CONNEXT_TOKENS:
                    continue

                # for Transfer topic
                sender, receiver = topic_args
                sender = hex(int(sender, 16))
                receiver = hex(int(receiver, 16))
                token = Token.address_lookup(_log["address"], chain)
                amount = int(_log["data"], 16) / (10**token.decimal)

                if sender == "0x0":
                    action = Action.MINT
                    user = receiver
                elif receiver == "0x0":
                    action = Action.BURN
                    user = sender
                else:
                    # let's focus on mint/burn count
                    # as criteria will be selected 
                    # based on CLP anyway
                    continue

                item = {
                    "timestamp": int(tx.timeStamp),
                    "chain": chain,
                    "hash": tx.hash,
                    "user_address": resolve_address(user),
                    "token_address": token.address,
                    "token_amount": amount,
                    "action": action,
                }
                fetched_items.append(item)

        # catch any error, add to error list
        except Exception as e:
            print_log(f"Error occured for tx: {tx.hash}")
            print_log(e)
            continue

    # add to mysql db
    insert_transactions(fetched_items, table_name)
    return fetched_items
    

def process_transfers(
    record: dict, 
) -> list:
    """
    Process a transaction record from AWS SQS
    """
    chain = record.get("chain")
    table_name = TABLE_NAME_MAPPER.get(chain)
    start_datetime = record.get("start_datetime")
    end_datetime = record.get("end_datetime")
    if not chain:
        raise Exception("Chain not found in queue record")
    start_block, end_block = get_block_range(chain, start_datetime, end_datetime)
    transfer_txs = []
    scan_api = ScanAPI(chain, apikey_schedule="random")
    for token in [Token.USDC, Token.WETH]:
        token_address = Token.get_lp(chain, token).address
        transfer_txs.extend(
            scan_api.get_transfer_events(
                token_address=token_address, 
                startblock=start_block,
                endblock=end_block,))

    fetched_items = []
    # iterate over all transactions
    for tx in transfer_txs:
        try:
            # filter non-liquidity txs
            tx_error = bool(tx.isError)
            if tx_error:
                print_log(f"Skipping transaction {tx.hash}")
                continue

            # resolve tx receipt
            print_log(f"Resolving transaction {tx.hash}")
            receipt = scan_api.get_transaction_receipt(
                tx.hash, max_attempt=10, wait_time=1)
            
            # skip if receipt is not available
            if isinstance(receipt, str):
                print_log(f"Error: {receipt}")
                continue

            # iterate over all logs
            logs = receipt["logs"]
            for _log in logs:
                topic, *topic_args = _log["topics"]
                topic_items = TOPIC2SIG.get(topic)

                # skip unknown topic name
                if topic_items is None:
                    continue

                topic_name, *topic_params = topic_items

                # filter unwanted topic
                if topic_name not in ["Transfer"]:
                    continue

                # skip blacklist address
                if _log["address"].lower() not in CONNEXT_TOKENS:
                    # skip if transfer aren't LP token
                    continue

                # for Transfer
                sender, receiver = topic_args
                sender = hex(int(sender, 16))
                receiver = hex(int(receiver, 16))
                token = Token.address_lookup(_log["address"], chain)
                if token is None:
                    continue
                amount = int(_log["data"], 16) / (10**token.decimal)

                fetched_items.append({
                    "timestamp": int(tx.timeStamp),
                    "chain": chain,
                    "hash": tx.hash,
                    "user_address": resolve_address(sender),
                    "token_address": token.address,
                    "token_amount": amount,
                    "action": Action.TRANSFER_OUT,
                })

                fetched_items.append({
                    "timestamp": int(tx.timeStamp),
                    "chain": chain,
                    "hash": tx.hash,
                    "user_address": resolve_address(receiver),
                    "token_address": token.address,
                    "token_amount": amount,
                    "action": Action.TRANSFER_IN,
                })

        # catch any error, add to error list
        except Exception as e:
            print_log(f"Error occured for tx: {tx.hash}")
            print_log(e)
            continue

    insert_transactions(fetched_items, table_name, )

    return fetched_items
