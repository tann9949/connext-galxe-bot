import logging
import os

import pymysql
from web3 import Web3, HTTPProvider
from web3.datastructures import AttributeDict

from .abi import connext_diamond_abi, erc20_abi
from .constant import Chain, DiamondContract


class SmartContract(object):

    default_providers = {
        Chain.ETHEREUM: "https://eth-rpc.gateway.pokt.network",
        Chain.OPTIMISM: "https://endpoints.omniatech.io/v1/op/mainnet/public",
        Chain.ARBITRUM_ONE: "https://endpoints.omniatech.io/v1/arbitrum/one/public",
        Chain.BNB_CHAIN: "https://bsc-dataseed3.binance.org",
        Chain.GNOSIS: "https://gnosis-mainnet.public.blastapi.io",
        Chain.POLYGON: "https://polygon-bor.publicnode.com",
    }
    
    @staticmethod
    def get_function_name(tx) -> str:
        return tx.functionName.split("(")[0]

    @staticmethod
    def get_default_provider(chain: Chain) -> Web3:
        return Web3(HTTPProvider(SmartContract.default_providers[chain]))

    def __init__(self, chain: Chain, address: str, abi: dict) -> None:
        self.provider = SmartContract.get_default_provider(chain)
        self.chain = chain

        self.address = address \
            if self.provider.is_checksum_address(address) \
            else self.provider.to_checksum_address(address)
        self.abi = abi
        self.contract = self.provider.eth.contract(self.address, abi=self.abi)

    @staticmethod
    def parse_bytes(item):
        if type(item) in [list, tuple]:
            item = [SmartContract.parse_bytes(_item) for _item in item]
        elif type(item) in [AttributeDict, dict]:
            item = {k: SmartContract.parse_bytes(v) for k, v in item.items()}
        elif isinstance(item, bytes):
            item = item.hex()
        return item

    def decode_input(self, input: str) -> dict:
        _, func_params = self.contract.decode_function_input(input)
        return {k: SmartContract.parse_bytes(v) for k, v in func_params.items()}


class ConnextDiamond(SmartContract):

    def __init__(self, chain: Chain) -> None:
        address = DiamondContract.get_contract_address(chain)
        super().__init__(chain, address, abi=connext_diamond_abi)


class ERC20Token(SmartContract):

    def __init__(
        self, 
        chain: Chain, 
        address: str,) -> None:
        super().__init__(chain, address, erc20_abi)
        self.load_data()

    def load_data(self):
        logging.debug(f"Loading token data from mysql: {self.address}, {self.chain}")
        with pymysql.connect(
            host=os.getenv("AWS_RDS_HOSTNAME"),
            user=os.getenv("AWS_RDS_USERNAME"),
            password=os.getenv("AWS_RDS_PASSWORD"),
            database="connext"
        ) as cnx:
            with cnx.cursor() as cursor:
                cursor.execute(
                    "SELECT name, symbol, `decimal` FROM Token WHERE address = %s AND chain = %s",
                    (self.address, int(self.chain))
                )
                row = cursor.fetchone()
                if row:
                    self.name, self.symbol, self.decimal = row
                else:
                    self.name = self.contract.functions.name().call()
                    self.symbol = self.contract.functions.symbol().call()
                    self.decimal = self.contract.functions.decimals().call()
                    self.total_supply = self.contract.functions.totalSupply().call()
                    self.save_data()
        
    def save_data(self):
        with pymysql.connect(
            host=os.getenv("AWS_RDS_HOSTNAME"),
            user=os.getenv("AWS_RDS_USERNAME"),
            password=os.getenv("AWS_RDS_PASSWORD"),
            database="connext"
        ) as cnx:
            with cnx.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO Token (name, symbol, address, `decimal`, chain) VALUES (%s, %s, %s, %s, %s)",
                        (self.name, self.symbol, self.address, int(self.decimal), int(self.chain))
                    )
                    cnx.commit()
