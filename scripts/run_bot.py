import importlib
import os

if importlib.util.find_spec("src") is None:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

if load_dotenv():
    print(".env loaded")

from src.bot.bot import ConnextTelegramBot
from src.constant import Chain
from src.erc20 import Token

# ROOT_DIR = "/home/ubuntu"
ROOT_DIR = "/Users/chompk.visai/Works/cdao/connext/connext-liquidity-dashboard"
LOG_FILE = f"{ROOT_DIR}/bot.log"
CACHE_PATH = f"{ROOT_DIR}/cache"
LP_TOKENS = [Token.CUSDCLP, Token.CWETHLP]
CHAINS = [
    Chain.ARBITRUM_ONE,
    Chain.BNB_CHAIN,
    Chain.OPTIMISM,
    Chain.GNOSIS,
    Chain.POLYGON
]


def main():
    bot = ConnextTelegramBot(
        cache_path=CACHE_PATH,
        log_path=LOG_FILE,
        chains=CHAINS
    )
    bot.run()


if __name__ == "__main__":
    main()
