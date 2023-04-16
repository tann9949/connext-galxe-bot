from __future__ import annotations


class Action:
    MINT = 1
    BURN = 2
    TRANSFER_IN = 3
    TRANSFER_OUT = 4


class Chain:
    ETHEREUM = 6648936
    OPTIMISM = 1869640809
    ARBITRUM_ONE = 1634886255
    BNB_CHAIN = 6450786
    GNOSIS = 6778479
    POLYGON = 1886350457
        
    @staticmethod
    def resolve_connext_domain(domain_id: int) -> Chain:
        if isinstance(domain_id, str):
            domain_id = int(domain_id)
        if domain_id == Chain.ETHEREUM:
            return "ethereum"
        elif domain_id == Chain.OPTIMISM:
            return "optimism"
        elif domain_id == Chain.ARBITRUM_ONE:
            return "arbitrum_one"
        elif domain_id == Chain.BNB_CHAIN:
            return "bnb_chain"
        elif domain_id == Chain.GNOSIS:
            return "gnosis"
        elif domain_id == Chain.POLYGON:
            return "polygon"
        else:
            raise Exception("Domain {domain_id} not supported")


class DiamondContract:
    ETHEREUM = "0x8898B472C54c31894e3B9bb83cEA802a5d0e63C6"
    OPTIMISM = "0x8f7492de823025b4cfaab1d34c58963f2af5deda"
    ARBITRUM_ONE = "0xEE9deC2712cCE65174B561151701Bf54b99C24C8"
    BNB_CHAIN = "0xCd401c10afa37d641d2F594852DA94C700e4F2CE"
    GNOSIS = "0x5bb83e95f63217cda6ae3d181ba580ef377d2109"
    POLYGON = "0x11984dc4465481512eb5b777E44061C158CF2259"

    @staticmethod
    def get_contract_address(chain: Chain) -> str:
        if chain == Chain.ETHEREUM:
            return DiamondContract.ETHEREUM
        elif chain == Chain.OPTIMISM:
            return DiamondContract.OPTIMISM
        elif chain == Chain.ARBITRUM_ONE:
            return DiamondContract.ARBITRUM_ONE
        elif chain == Chain.BNB_CHAIN:
            return DiamondContract.BNB_CHAIN
        elif chain == Chain.GNOSIS:
            return DiamondContract.GNOSIS
        elif chain == Chain.POLYGON:
            return DiamondContract.POLYGON
        else:
            raise Exception("Chain {chain} not supported")
