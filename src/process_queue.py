import os
from datetime import datetime

import pymysql

from .utils import print_log
from .constant import Action, Chain, DiamondContract
from .scan import ScanAPI
from .erc20 import Token
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
    "removeSwapLiquidity",
    "removeSwapLiquidityImbalance",
    "removeSwapLiquidityOneToken",
]
TOPICS = [ "Transfer" ]

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
    exist_check: bool = True,
    epsilon: float = 0.00001
) -> None:
    print(f"[+] Adding {len(fetched_items)} items to mysql db")
    cnx = pymysql.connect(
        host=os.getenv("AWS_RDS_HOSTNAME"),
        user=os.getenv("AWS_RDS_USERNAME"),
        password=os.getenv("AWS_RDS_PASSWORD"),
        database="connext"
    )
    print_log(f"[-] db connection established")
    # add to mysql db
    for item in fetched_items:
        with cnx.cursor() as cursor:
            print_log(f"[-] Adding {item} to {table_name}")

            if exist_check:
                query = (
                    f"SELECT * FROM {table_name} "
                    f"WHERE hash='{item['hash']}' AND user_address='{item['user_address']}' AND token_address='{item['token_address']}' AND "
                    f"(token_amount={item['token_amount']} OR ABS(token_amount-{item['token_amount']}) < {epsilon}) AND "
                    f"action={item['action']} AND timestamp={item['timestamp']} AND chain={item['chain']}"
                )
                cursor.execute(query)
                print_log(f"[-] Found a total of {cursor.rowcount} records")
                if cursor.rowcount > 0:
                    print_log(f"[-] {cursor.rowcount} record already exists. Skipping...")
                    continue
            
            print_log("[-] Inserting record into db, constructing query...")
            query = (
                f"INSERT INTO {table_name} "
                "(timestamp, chain, hash, user_address, token_address, token_amount, action) "
                f"VALUES ({item['timestamp']}, {item['chain']}, '{item['hash']}', '{item['user_address']}', "
                f"'{item['token_address']}', {item['token_amount']}, {item['action']})"
            )
            print_log(f"[-] query: {query}")
            cursor.execute(query)
            cnx.commit()
            print_log(f"[-] {cursor.rowcount} record inserted.")


def get_whitelist_tokens(chain: Chain, cast_lower: bool = True) -> list:
    whitelist_tokens = []
    for token_type in Token.address_mapper[chain].values():
        for _token in token_type.values():
            _addr = _token.address
            if cast_lower:
                _addr = _addr.lower()
            
            whitelist_tokens.append(_addr)
    return whitelist_tokens


def process_transaction(
    record: dict, 
    exist_check: bool = True,
) -> list:
    """
    Process a transaction record from AWS SQS
    """
    print_log("[+] Processing transaction record")
    print_log(f"[-] Enabling exist check: {exist_check}")
    chain = int(record.get("chain"))
    table_name = TABLE_NAME_MAPPER.get(chain)
    start_datetime = record.get("start_datetime")
    end_datetime = record.get("end_datetime")
    whitelist_tokens = get_whitelist_tokens(chain)
    print_log(f"[-] Chain: {Chain.resolve_connext_domain(chain)}")
    print_log(f"[-] Time fetch: {start_datetime} -> {end_datetime}")
    print_log(f"[-] Table: {table_name}")
    print_log(f"[-] Whitelist tokens: {whitelist_tokens}")
    if not chain:
        raise Exception("Chain not found in queue record")
    scan_api = ScanAPI(chain, apikey_schedule="random")
    
    start_block, end_block = get_block_range(chain, start_datetime, end_datetime)
    print_log(f"[-] Block fetch: {start_block} -> {end_block}")
    txs = scan_api.get_transaction_by_address(
        DiamondContract.get_contract_address(chain),
        startblock=start_block,
        endblock=end_block,
    )

    fetched_items = []
    # iterate over all transactions
    print(f"[+] Processing {len(txs)} transactions from ConnextDiamond contract")
    for tx in txs:
        try:
            # filter non-liquidity txs
            tx_error = bool(tx.isError)
            tx_function = tx.functionName.split("(")[0]
            if tx_error or tx_function not in FUNCTIONS:
                print_log(f"[-] Skipping {tx_function} transaction {tx.hash}")
                continue

            # skip if transaction already have receipt
            if tx.logs is not None:
                continue

            # resolve tx receipt
            print_log(f"[-] Resolving transaction {tx.hash}")
            receipt = scan_api.get_transaction_receipt(
                tx.hash, max_attempt=10, wait_time=1)
            
            # skip if receipt is not available
            if isinstance(receipt, str):
                print_log(f"[+] Error: {receipt}")
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
                    print_log(f"[-] Skipping {topic_name} topic")
                    continue

                # skip unwanted address
                if _log["address"].lower() not in whitelist_tokens:
                    print_log(f"[-] Skipping {_log['address']} address")
                    continue

                print_log(f"[-] Processing {topic_name} topic for token {_log['address']}")

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
            print_log(f"[+] Error occured for tx: {tx.hash}")
            print_log(e)
            continue

    # add to mysql db
    insert_transactions(fetched_items, table_name, exist_check=exist_check)
    return fetched_items
    

def process_transfers(
    record: dict, 
    exist_check: bool = True,
) -> list:
    """
    Process a transaction record from AWS SQS
    """
    print_log("[+] Processing transfers record")
    print_log(f"[-] Enabling exist check: {exist_check}")
    chain = record.get("chain")
    lp_tokens = [
        Token.get_lp(chain, _token).address.lower().strip() 
        for _token in [Token.USDC, Token.WETH]]
    table_name = TABLE_NAME_MAPPER.get(chain)
    start_datetime = record.get("start_datetime")
    end_datetime = record.get("end_datetime")
    print_log(f"[-] Chain: {Chain.resolve_connext_domain(chain)}")
    print_log(f"[-] Time fetch: {start_datetime} -> {end_datetime}")
    print_log(f"[-] Table: {table_name}")
    if not chain:
        raise Exception("Chain not found in queue record")
    start_block, end_block = get_block_range(chain, start_datetime, end_datetime)
    print_log(f"[-] Block fetch: {start_block} -> {end_block}")

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
    print(f"[+] Processing {len(transfer_txs)} transactions from ConnextDiamond contract")
    # iterate over all transactions
    for tx in transfer_txs:
        try:
            # filter non-liquidity txs
            tx_error = bool(tx.isError)
            if tx_error:
                print_log(f"[-] Skipping transfers transaction {tx.hash}")
                continue

            # resolve tx receipt
            print_log(f"[-] Resolving transaction {tx.hash}")
            receipt = scan_api.get_transaction_receipt(
                tx.hash, max_attempt=10, wait_time=1)
            
            # skip if receipt is not available
            if isinstance(receipt, str):
                print_log(f"[+] Error: {receipt}")
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
                if _log["address"].lower() not in lp_tokens:
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
            print_log(f"[+] Error occured for tx: {tx.hash}")
            print_log(e)
            continue

    insert_transactions(fetched_items, table_name, exist_check=exist_check)

    return fetched_items
