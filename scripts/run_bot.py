import itertools
import os
import time
from datetime import datetime
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from telegram import Update
from telegram.ext import Application, CallbackContext, CommandHandler
from telegram.error import NetworkError

if load_dotenv():
    print(".env loaded")

from src.token import Token
from src.constant import Chain
from src.utils import print_log
from src.process_queue import TABLE_NAME_MAPPER


LOG_FILE = "/home/ubuntu/bot.log"
CACHE_PATH = "/home/ubuntu/cache"
CAMPAIGN_START_DATETIME = datetime.fromtimestamp(1676419200)
LP_TOKENS = [Token.CUSDCLP, Token.CWETHLP]
CHAINS = [
    Chain.ARBITRUM_ONE,
    Chain.BNB_CHAIN,
    Chain.OPTIMISM,
    Chain.GNOSIS,
    Chain.POLYGON
]


def resolve_action(action: int) -> str:
    action = int(action)
    if action == 1:
        return "mint"
    elif action == 2:
        return "burn"
    elif action == 3:
        return "transfer_in"
    elif action == 4:
        return "transfer_out"


def load_cache() -> pd.DataFrame:
    dataset = []
    for chain in CHAINS:
        df = pd.read_csv(
            f"{CACHE_PATH}/{Chain.resolve_connext_domain(chain)}_user_scores.csv"
        )
        df["chain"] = Chain.resolve_connext_domain(chain)
        dataset.append(df)
    return pd.concat(dataset, axis=0).reset_index(drop=True)


def query_user(
    query: str, 
    user_scores: Optional[pd.DataFrame],
    min_usdc_value: float = 0, 
    min_weth_value: float = 0,
    threshold: float = 0.3
) -> None:
    query = query.lower().strip()
    results = {
        "wallet": query
    }
    
    filters = {}
    if min_usdc_value > 0:
        print_log(f"Applying filter for with {min_usdc_value} CUSDCLP")
        filters["usdc"] = min_usdc_value
    if min_weth_value > 0:
        print_log(f"Applying filter for with {min_weth_value} CWETHLP")
        filters["weth"] = min_weth_value
    results["filters"] = filters
    
    query_results = {}
    for chain, token in itertools.product(CHAINS, LP_TOKENS):
        min_value = min_usdc_value if token == Token.CUSDCLP else min_weth_value
        chain = Chain.resolve_connext_domain(chain)
        _score = user_scores[(user_scores["chain"] == chain) & (user_scores["token"] == token)].sort_values(
            "balance_change", ascending=False).reset_index(drop=True)
        qualified = _score.iloc[:round(len(_score[_score["balance_change"] > min_value]) * threshold)]
        user_results = qualified[qualified["user_address"] == query]
        
        if len(user_results) > 0:
            query_results[f"{chain}_{token}"] = {
                "rank": user_results.index[0],
                "score": user_results["balance_change"].values[0],
                "qualified": len(qualified)
            }
    results["results"] = query_results
    return {
        "statusCode": 200,
        "body": results
    }


def format_results(wallet: str, results: dict) -> str:
    template = f"Wallet address: {wallet}\n\n"

    chain_qualified = []
    for k, v in results["results"].items():
        items = k.split("_")
        token = items[-1]
        chain = " ".join(items[:-1])
        rank = v["rank"]
        score = v["score"]
        n_qualified = v["qualified"]

        template += f"You are qualified for {token} on {chain}\n"
        template += f"Rank [{rank} / {n_qualified}]\n"
        if token == Token.CUSDCLP:
            template += f"Your score: {score:.2f}\n\n"
        elif token == Token.CWETHLP:
            template += f"Your score: {score:.6f}\n\n"

        chain_qualified.append(chain)

    template += f"You've qualified {len(chain_qualified)} chains!\n"
    template += f"{chain_qualified}"
    return template



async def score_callback(update: Update, context: CallbackContext) -> None:
    curr_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    args = context.args
    if len(args) != 1:
        await reply_message(update,
                     f"Please add your wallet as an argument!\ne.g. /score <wallet>")
        return
    
    wallet = args[0].lower().strip()

    print_log(f"[{curr_time}] Querying {wallet}")
    results = query_user(wallet, load_cache())
    template = format_results(wallet, results["body"])

    with open(LOG_FILE, "a") as fp:
        fp.write(f"{curr_time},score")
    await reply_message(
        update,
        template
    )


async def score_filter_callback(update: Update, context: CallbackContext) -> None:
    curr_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    args = context.args
    if len(args) != 3:
        await reply_message(update,
                     f"Please add your wallet and minimum USDC/WETH filter as an argument!\ne.g. /score_filter <min-usdc> <min-weth> <wallet>")
        return
    
    wallet = args[-1].lower().strip()
    try:
        min_usdc = float(args[0].strip())
    except ValueError:
        await reply_message(update,
                     f"<min-usdc> must be in a float (numerical) format! {args}")
        return
    
    try:
        min_weth = float(args[1].strip())
    except ValueError:
        await reply_message(update,
                     f"<min-weth> must be in a float (numerical) format {args}")
        return

    print_log(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Querying {wallet}, fillter {min_usdc} USDC, {min_weth} WETH")
    results = query_user(wallet, load_cache(), min_usdc_value=min_usdc, min_weth_value=min_weth)
    template = format_results(wallet, results["body"])

    with open(LOG_FILE, "a") as fp:
        fp.write(f"{curr_time},score_filter")
    await reply_message(
        update,
        template
    )


async def reply_message(update: Update, message: str) -> None:
    if update.message is not None:
        await update.message.reply_text(
            text=message
        )
    else:
        print_log("update.message is None!")
    # is_sent = False
    # while not is_sent:
    #     try:
    #         await update.message.reply_text(
    #             text=message
    #         )
    #     except NetworkError as e:
    #         print_log("Error sending message. Retrying in 0.5 seconds")
    #         print_log(e)
    #         time.sleep(0.5)
    #         continue


def plot_user(query: str, timeframe: str = "T") -> None:
    dataset = load_dataset()
    latest_date = dataset.index.max()
    user_txs = dataset[dataset["user_address"] == query.lower().strip()]
    save_path = f"/home/ubuntu/cache/img/{query}.png"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    if len(user_txs["token"].unique()) == 1:
    
        fig, ax = plt.subplots(1, 1, figsize=(13, 4))
        _token = user_txs["token"].unique()[0]

        temp = pd.Series(
            data=[0., 0.], 
            index=[CAMPAIGN_START_DATETIME, latest_date], 
            name="balance_change")
        for _chain in list(map(Chain.resolve_connext_domain, CHAINS)):
            _data = dataset[
                (dataset["user_address"] == query.lower()) & \
                (dataset["chain"] == _chain) & \
                (dataset["token"] == _token)
            ]
            if len(_data) > 0:
                _data = pd.concat([_data, pd.DataFrame([{
                    "hash": "",
                    "user_address": query,
                    "token_amount": 0,
                    "action": "",
                    "balance_change": 0
                }, {
                    "hash": "",
                    "user_address": query,
                    "token_amount": 0,
                    "action": "",
                    "balance_change": 0
                }], index=[CAMPAIGN_START_DATETIME, latest_date])], axis=0)
                _data = _data.sort_index()
                _data = _data["balance_change"].cumsum().resample(timeframe).last().ffill()
                _data = _data[_data.index >= CAMPAIGN_START_DATETIME]
                _data.plot(ax=ax, label=_chain)
                ax.legend()
            ax.set_title(f"{_token} Balance")
        fig.suptitle(query)
    elif len(user_txs["token"].unique()) > 1:

        fig, ax = plt.subplots(1, 2, figsize=(13, 4))

        temp = pd.Series(
            data=[0., 0.], 
            index=[CAMPAIGN_START_DATETIME, latest_date], 
            name="balance_change")
        for i, _token in enumerate(LP_TOKENS):
            for _chain in list(map(Chain.resolve_connext_domain, CHAINS)):
                _data = dataset[
                    (dataset["user_address"] == query.lower()) & \
                    (dataset["chain"] == _chain) & \
                    (dataset["token"] == _token)
                ]
                if len(_data) > 0:
                    _data = pd.concat([_data, pd.DataFrame([{
                        "hash": "",
                        "user_address": query,
                        "token_amount": 0,
                        "action": "",
                        "balance_change": 0
                    }, {
                        "hash": "",
                        "user_address": query,
                        "token_amount": 0,
                        "action": "",
                        "balance_change": 0
                    }], index=[CAMPAIGN_START_DATETIME, latest_date])], axis=0)
                    _data = _data.sort_index()
                    _data = _data["balance_change"].cumsum().resample(timeframe).last().ffill()
                    _data = _data[_data.index >= CAMPAIGN_START_DATETIME]
                    _data.plot(ax=ax[i], label=_chain)
                    ax[i].legend()
            ax[i].set_title(f"{_token} Balance")
        fig.suptitle(query)
    fig.savefig(save_path)
    return save_path


def load_dataset():
    df = pd.read_csv(f"/home/ubuntu/cache/full_dataset.csv")
    df["datetime"] = df["datetime"].map(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
    df = df.set_index("datetime").sort_index()
    return df


async def stats_callback(update: Update, context: CallbackContext) -> None:
    curr_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    args = context.args
    if len(args) != 1:
        await reply_message(update,
                     f"Please add your wallet as an argument!\ne.g. /score <wallet>")
        return
    
    wallet = args[0].lower().strip()

    print_log(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Getting stats {wallet}")
    fig_path = plot_user(wallet)
    with open(LOG_FILE, "a") as fp:
        fp.write(f"{curr_time},stats")
    await reply_image(
        update,
        fig_path
    )
    os.remove(fig_path)

async def reply_image(update: Update, img_path: str) -> None:
    if update.message is not None:
        await update.message.reply_photo(
            photo=img_path
        )
    else:
        print_log("update.message is None!")


def main():
    app = Application.builder().token(
        token=os.getenv("TELEGRAM_BOT_TOKEN")
    ).build()

    app.add_handler(
        CommandHandler(
            "score",
            score_callback
        )
    )

    app.add_handler(
        CommandHandler(
            "stats",
            stats_callback
        )
    )

    app.add_handler(
        CommandHandler(
            "score_filter",
            score_filter_callback
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
