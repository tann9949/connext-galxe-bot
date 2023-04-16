from __future__ import annotations
from typing import Optional

from .contract import ERC20Token
from .constant import Chain


class Token:
    USDC = "USDC"
    WETH = "WETH"
    CUSDCLP = "CUSDCLP"
    CWETHLP = "CWETHLP"

    address_mapper = {
        Chain.ETHEREUM: {
            "canonical": {
                USDC: "",
                WETH: "",
            },
            "next": {
                USDC: "",
                WETH: "",
            },
            "lp": {
                CUSDCLP: "",
                CWETHLP: "",
            }
        },
        Chain.BNB_CHAIN: {
            "canonical": {
                USDC: ERC20Token(Chain.BNB_CHAIN, "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d"),
                WETH: ERC20Token(Chain.BNB_CHAIN, "0x2170Ed0880ac9A755fd29B2688956BD959F933F8"),
            },
            "next": {
                USDC: ERC20Token(Chain.BNB_CHAIN, "0x5e7D83dA751F4C9694b13aF351B30aC108f32C38"),
                WETH: ERC20Token(Chain.BNB_CHAIN, "0xA9CB51C666D2AF451d87442Be50747B31BB7d805"),
            },
            "lp": {
                USDC: ERC20Token(Chain.BNB_CHAIN, "0xc170908481E928DfA39DE3D0d31bEa6292692F8e"),
                WETH: ERC20Token(Chain.BNB_CHAIN, "0x223F6A3B8d087741BF99a2531DC53cd15745eBa7"),
            }
        },
        Chain.POLYGON: {
            "canonical": {
                USDC: ERC20Token(Chain.POLYGON, "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"),
                WETH: ERC20Token(Chain.POLYGON, "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619"),
            },
            "next": {
                USDC: ERC20Token(Chain.POLYGON, "0xF96C6d2537e1af1a9503852eB2A4AF264272a5B6"),
                WETH: ERC20Token(Chain.POLYGON, "0x4b8BaC8Dd1CAA52E32C07755c17eFadeD6A0bbD0"),
            },
            "lp": {
                USDC: ERC20Token(Chain.POLYGON, "0xa03258b76Ef13AF716370529358f6A79eb03ec12"),
                WETH: ERC20Token(Chain.POLYGON, "0xeF1348dAC70e8349513E4Ae7498F302e27102101"),
            }
        },
        Chain.OPTIMISM: {
            "canonical": {
                USDC: ERC20Token(Chain.OPTIMISM, "0x7F5c764cBc14f9669B88837ca1490cCa17c31607"),
                WETH: ERC20Token(Chain.OPTIMISM, "0x4200000000000000000000000000000000000006"),
            },
            "next": {
                USDC: ERC20Token(Chain.OPTIMISM, "0x67E51f46e8e14D4E4cab9dF48c59ad8F512486DD"),
                WETH: ERC20Token(Chain.OPTIMISM, "0xbAD5B3c68F855EaEcE68203312Fd88AD3D365e50"),
            },
            "lp": {
                USDC: ERC20Token(Chain.OPTIMISM, "0xB12A1Be740B99D845Af98098965af761be6BD7fE"),
                WETH: ERC20Token(Chain.OPTIMISM, "0x3C12765d3cFaC132dE161BC6083C886B2Cd94934"),
            }
        },
        Chain.ARBITRUM_ONE: {
            "canonical": {
                USDC: ERC20Token(Chain.ARBITRUM_ONE, "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8"),
                WETH: ERC20Token(Chain.ARBITRUM_ONE, "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1"),
            },
            "next": {
                USDC: ERC20Token(Chain.ARBITRUM_ONE, "0x8c556cF37faa0eeDAC7aE665f1Bb0FbD4b2eae36"),
                WETH: ERC20Token(Chain.ARBITRUM_ONE, "0x2983bf5c334743Aa6657AD70A55041d720d225dB"),
            },
            "lp": {
                USDC: ERC20Token(Chain.ARBITRUM_ONE, "0xDa492C29D88FfE9B7cbfA6DC068C2f9befaE851b"),
                WETH: ERC20Token(Chain.ARBITRUM_ONE, "0xb86AF5eB59A8e871bfA573FA656123ea86F47c3a"),
            }
        },
        Chain.GNOSIS: {
            "canonical": {
                USDC: ERC20Token(Chain.GNOSIS, "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83"),
                WETH: ERC20Token(Chain.GNOSIS, "0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1"),
            },
            "next": {
                USDC: ERC20Token(Chain.GNOSIS, "0x44CF74238d840a5fEBB0eAa089D05b763B73faB8"),
                WETH: ERC20Token(Chain.GNOSIS, "0x538E2dDbfDf476D24cCb1477A518A82C9EA81326"),
            },
            "lp": {
                USDC: ERC20Token(Chain.GNOSIS, "0xA639FB3f8C52e10E10a8623616484d41765d5F82"),
                WETH: ERC20Token(Chain.GNOSIS, "0x7aC5bBefAE0459F007891f9Bd245F6beaa91076c"),
            }
        },
    }

    @staticmethod
    def address_lookup(address: str, chain: Chain) -> Optional[ERC20Token]:
        for token in Token.address_mapper[chain]["canonical"].values():
            if token.address.lower() == address.lower():
                return token
        for token in Token.address_mapper[chain]["next"].values():
            if token.address.lower() == address.lower():
                return token
        for token in Token.address_mapper[chain]["lp"].values():
            if token.address.lower() == address.lower():
                return token
        return None

    @staticmethod
    def get_canonical(chain: Chain, token: str) -> ERC20Token:
        return Token.address_mapper[chain]["canonical"][token]

    @staticmethod
    def get_next(chain: Chain, token: str) -> ERC20Token:
        return Token.address_mapper[chain]["next"][token]

    @staticmethod
    def get_lp(chain: Chain, token: str) -> ERC20Token:
        return Token.address_mapper[chain]["lp"][token]
