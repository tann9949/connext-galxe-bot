import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pymysql
from dotenv import load_dotenv
from web3 import Web3, HTTPProvider

from src.abi import erc20_abi
from src.utils import print_log

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
        "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",  # canonical DAI
        "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58",  # canonical USDT
        "0xd64Bd028b560bbFc732eA18f282c64B86F3468e0",  # next DAI
        "0x4cBB28FA12264cD8E87C62F4E1d9f5955Ce67D20",  # next USDT
        "0xeD6d021DcA3d31D63997e4985fa6Eb3A2B745472",  # CDAILP
        "0x2C7FA89CC5Ea38d4e5193512b9C10808348Ba74F",  # CUSDTLP
        "0x67E51f46e8e14D4E4cab9dF48c59ad8F512486DD",  # next USDC
        "0xbAD5B3c68F855EaEcE68203312Fd88AD3D365e50",  # next WETH
        "0xB12A1Be740B99D845Af98098965af761be6BD7fE",  # CUSDCLP
        "0x3C12765d3cFaC132dE161BC6083C886B2Cd94934",  # CWETHLP
    ],
    Chain.ARBITRUM_ONE: [
        "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8",  # canonical USDC
        "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",  # canonical WETH
        "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",  # canonical DAI
        "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",  # canonical USDT
        "0xfDe99b3B3fbB69553D7DaE105EF34Ba4FE971190",  # next DAI
        "0x2fD7E61033b3904c65AA9A9B83DCd344Fa19Ffd2",  # next USDT
        "0x61B3184be0c95324BF00e0DE12765B5f6Cc6b7cA",  # CDAILP
        "0x45d0736D77A72AE2Bd3c5770878bd85b72895057",  # CUSDTLP
        "0x8c556cF37faa0eeDAC7aE665f1Bb0FbD4b2eae36",  # next USDC
        "0x2983bf5c334743Aa6657AD70A55041d720d225dB",  # next WETH
        "0xDa492C29D88FfE9B7cbfA6DC068C2f9befaE851b",  # CUSDCLP
        "0xb86AF5eB59A8e871bfA573FA656123ea86F47c3a",  # CWETHLP
    ],
    Chain.BNB_CHAIN: [
        "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",  # canonical USDC
        "0x2170Ed0880ac9A755fd29B2688956BD959F933F8",  # canonical WETH
        "0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3",  # canonical DAI
        "0x55d398326f99059fF775485246999027B3197955",  # canonical USDT
        "0x86a343BCF17D79C475d300eed35F0145F137D0c9",  # next DAI
        "0xD609f26B5547d5E31562B29150769Cb7c774B97a",  # next USDT
        "0xf9D88D200f3D9B45Bd9f8f3ae124f59a4fbdbae5",  # CDAILP
        "0x9350470389848979fCdFEd28352Ff9e0C9Aa87e9",  # CUSDTLP
        "0x5e7D83dA751F4C9694b13aF351B30aC108f32C38",  # next USDC
        "0xA9CB51C666D2AF451d87442Be50747B31BB7d805",  # next WETH
        "0xc170908481E928DfA39DE3D0d31bEa6292692F8e",  # CUSDCLP
        "0x223F6A3B8d087741BF99a2531DC53cd15745eBa7",  # CWETHLP
    ],
    Chain.POLYGON: [
        "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",  # canonical USDC
        "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",  # canonical WETH
        "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",  # canonical DAI
        "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",  # canonical USDT
        "0xaDCe87b14d570665222C1172D18a221BF7690d5a",  # next DAI
        "0xE221C5A2a8348f12dcb2b0e88693522EbAD2690f",  # next USDT
        "0xe6228819A3416a256DFEF2568A75737046438cB8",  # CDAILP
        "0x7F7948B1345b6A95b65a001278b480CE12cA66E5",  # CUSDTLP
        "0xF96C6d2537e1af1a9503852eB2A4AF264272a5B6",  # next USDC
        "0x4b8BaC8Dd1CAA52E32C07755c17eFadeD6A0bbD0",  # next WETH
        "0xa03258b76Ef13AF716370529358f6A79eb03ec12",  # CUSDCLP
        "0xeF1348dAC70e8349513E4Ae7498F302e27102101",  # CWETHLP
    ],
    Chain.GNOSIS: [
        "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83",  # canonical USDC
        "0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1",  # canonical WETH
        "0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d",  # canonical DAI
        "0x4ECaBa5870353805a9F068101A40E0f32ed605C6",  # canonical USDT
        "0x0e1D5Bcd2Ac5CF2f71841A9667afC1E995CaAf4F",  # next DAI
        "0xF4d944883D6FddC56d3534986feF82105CaDbfA1",  # next USDT
        "0x98f7656A6C09388c646ff423ED82980675a152dD",  # CDAILP
        "0xD8a772fD2B7872230cCD92EF073bE81De87137D7",  # CUSDTLP
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
        address: str, ) -> None:
        self.provider = ERC20Token.get_default_provider(chain)

        self.address = address \
            if self.provider.is_checksum_address(address) \
            else self.provider.to_checksum_address(address)

        self.abi = erc20_abi
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
    cnx = pymysql.connect(
        host=os.getenv("AWS_RDS_HOSTNAME"),
        user=os.getenv("AWS_RDS_USERNAME"),
        password=os.getenv("AWS_RDS_PASSWORD"),
        database="connext"
    )
    for chain, tokens in TOKENS.items():
        print_log(f"[+] Checking tokens from {chain}...")
        for token_address in tokens:
            token_contract = ERC20Token(chain, token_address)

            name = token_contract.name
            symbol = token_contract.symbol
            address = token_contract.address
            decimal = token_contract.decimal

            print_log(f"[+] Checking {name} ({symbol}) from {chain} to database...")

            with cnx.cursor() as cursor:
                # check if token existed by address,chain
                if cursor.execute("SELECT * FROM Token WHERE address = %s AND chain = %s", (address, int(chain))):
                    print_log(f"[-] {name} ({symbol}) from {chain} already existed in database, skipping...")
                else:
                    print_log(f"[-] Adding {name} ({symbol}) from {chain} to database")
                    cursor.execute(
                        "INSERT INTO Token (name, symbol, address, `decimal`, chain) VALUES (%s, %s, %s, %s, %s)",
                        (name, symbol, address, int(decimal), int(chain))
                    )
                    cnx.commit()


if __name__ == "__main__":
    main()
