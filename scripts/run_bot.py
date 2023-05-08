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

CHAINS = [
    Chain.ARBITRUM_ONE,
    Chain.BNB_CHAIN,
    Chain.OPTIMISM,
    Chain.GNOSIS,
    Chain.POLYGON
]


def main():
    root_dir = os.getenv("ROOT_DIR", "/home/ubuntu")
    log_path = f"{root_dir}/bot.log"
    cache_path = f"{root_dir}/cache"

    bot = ConnextTelegramBot(
        cache_path=cache_path,
        log_path=log_path,
        chains=CHAINS
    )
    bot.run()


if __name__ == "__main__":
    main()
