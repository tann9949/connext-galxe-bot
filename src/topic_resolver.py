from .abi import connext_diamond_abi, erc20_abi
from .constant import Chain
from .contract import SmartContract


def get_topic_resolver():
    abis = connext_diamond_abi + erc20_abi
    provider = SmartContract.get_default_provider(Chain.ETHEREUM)
    
    topic2sig = {}
    for abi in abis:
        name = abi["name"]
        inputs = ",".join([_item["type"] for _item in abi["inputs"]])
        sig = f"{name}({inputs})"
        topic_id = provider.to_hex(provider.keccak(text=sig))

        topic2sig[topic_id] = [name] + [_item["type"] for _item in abi["inputs"]]
    return topic2sig
