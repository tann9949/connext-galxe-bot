import json
import os

import mysql.connector
from dotenv import load_dotenv
from web3 import Web3, HTTPProvider

load_dotenv()


class Chain:
    ETHEREUM = 6648936
    OPTIMISM = 1869640809
    ARBITRUM_ONE = 1634886255
    BNB_CHAIN = 6450786
    GNOSIS = 6778479
    POLYGON = 1886350457


TOKENS = {
    Chain.OPTIMISM: [
        "0x7F5c764cBc14f9669B88837ca1490cCa17c31607",  # canonical USDC
        "0x4200000000000000000000000000000000000006",  # canonical WETH
        "0x67E51f46e8e14D4E4cab9dF48c59ad8F512486DD",  # next USDC
        "0xbAD5B3c68F855EaEcE68203312Fd88AD3D365e50",  # next WETH
        "0xB12A1Be740B99D845Af98098965af761be6BD7fE",  # CUSDCLP
        "0x3C12765d3cFaC132dE161BC6083C886B2Cd94934",  # CWETHLP
    ],
    Chain.ARBITRUM_ONE: [
        "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8",  # canonical USDC
        "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",  # canonical WETH
        "0x8c556cF37faa0eeDAC7aE665f1Bb0FbD4b2eae36",  # next USDC
        "0x2983bf5c334743Aa6657AD70A55041d720d225dB",  # next WETH
        "0xDa492C29D88FfE9B7cbfA6DC068C2f9befaE851b",  # CUSDCLP
        "0xb86AF5eB59A8e871bfA573FA656123ea86F47c3a",  # CWETHLP
    ],
    Chain.BNB_CHAIN: [
        "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",  # canonical USDC
        "0x2170Ed0880ac9A755fd29B2688956BD959F933F8",  # canonical WETH
        "0x5e7D83dA751F4C9694b13aF351B30aC108f32C38",  # next USDC
        "0xA9CB51C666D2AF451d87442Be50747B31BB7d805",  # next WETH
        "0xc170908481E928DfA39DE3D0d31bEa6292692F8e",  # CUSDCLP
        "0x223F6A3B8d087741BF99a2531DC53cd15745eBa7",  # CWETHLP
    ],
    Chain.POLYGON: [
        "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",  # canonical USDC
        "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",  # canonical WETH
        "0xF96C6d2537e1af1a9503852eB2A4AF264272a5B6",  # next USDC
        "0x4b8BaC8Dd1CAA52E32C07755c17eFadeD6A0bbD0",  # next WETH
        "0xa03258b76Ef13AF716370529358f6A79eb03ec12",  # CUSDCLP
        "0xeF1348dAC70e8349513E4Ae7498F302e27102101",  # CWETHLP
    ],
    Chain.GNOSIS: [
        "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83",  # canonical USDC
        "0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1",  # canonical WETH
        "0x44CF74238d840a5fEBB0eAa089D05b763B73faB8",  # next USDC
        "0x538E2dDbfDf476D24cCb1477A518A82C9EA81326",  # next WETH
        "0xA639FB3f8C52e10E10a8623616484d41765d5F82",  # CUSDCLP
        "0x7aC5bBefAE0459F007891f9Bd245F6beaa91076c",  # CWETHLP
    ],
}


class ERC20Token(object):

    default_providers = {
        Chain.ETHEREUM: "https://eth-rpc.gateway.pokt.network",
        Chain.OPTIMISM: "https://endpoints.omniatech.io/v1/op/mainnet/public",
        Chain.ARBITRUM_ONE: "https://endpoints.omniatech.io/v1/arbitrum/one/public",
        Chain.BNB_CHAIN: "https://bsc-dataseed3.binance.org",
        Chain.GNOSIS: "https://gnosis-mainnet.public.blastapi.io",
        Chain.POLYGON: "https://polygon-bor.publicnode.com",
    }

    def __init__(
        self, 
        chain: Chain, 
        address: str, 
        abi_path: str = "./abi/erc20.json",) -> None:
        self.provider = ERC20Token.get_default_provider(chain)

        self.address = address \
            if self.provider.is_checksum_address(address) \
            else self.provider.to_checksum_address(address)

        with open(abi_path, "r") as fp:
            self.abi = json.load(fp)

        self.contract = self.provider.eth.contract(self.address, abi=self.abi)

        self.load_data()

    @staticmethod
    def get_default_provider(chain: Chain) -> Web3:
        return Web3(HTTPProvider(ERC20Token.default_providers[chain]))

    def load_data(self):
        self.name = self.contract.functions.name().call()
        self.symbol = self.contract.functions.symbol().call()
        self.decimal = self.contract.functions.decimals().call()


def main():
    cnx = mysql.connector.connect(
        host=os.getenv("AWS_RDS_HOSTNAME"),
        user=os.getenv("AWS_RDS_USERNAME"),
        password=os.getenv("AWS_RDS_PASSWORD"),
        database="connext"
    )
    for chain, tokens in TOKENS.items():
        for token_address in tokens:
            token_contract = ERC20Token(chain, token_address)

            name = token_contract.name
            symbol = token_contract.symbol
            address = token_contract.address
            decimal = token_contract.decimal

            print(f"Adding {name} ({symbol}) from {chain} to database...")

            with cnx.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Token (name, symbol, address, `decimal`, chain) VALUES (%s, %s, %s, %s, %s)",
                    (name, symbol, address, int(decimal), int(chain))
                )
                cnx.commit()


if __name__ == "__main__":
    main()
