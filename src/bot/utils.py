import itertools
import os
import time
from typing import List, Optional

import matplotlib.pyplot as plt
import pandas as pd
from telegram import Update
from telegram.error import NetworkError

from src.campaign import CAMPAIGNS, get_checkpoint_dates
from src.constant import Chain
from src.erc20 import Token
from src.utils import print_log


async def reply_image(update: Update, img_path: str) -> None:
    if update.message is not None:
        await update.message.reply_photo(
            photo=img_path
        )
    else:
        print_log("update.message is None!")


async def reply_markdown(update: Update, message: str) -> None:
    if update.message is not None:
        await update.message.reply_markdown_v2(
            text=message
        )
    else:
        print_log("update.message is None!")


async def reply_message(update: Update, message: str, do_retry: bool = False) -> None:
    if do_retry:
        # send message with retries
        is_sent = False
        while not is_sent:
            try:
                await update.message.reply_text(
                    text=message
                )
            except NetworkError as e:
                print_log("Error sending message. Retrying in 0.5 seconds")
                print_log(e)
                time.sleep(0.5)
                continue
    else:
        # send message without retry
        if update.message is not None:
            await update.message.reply_text(
                text=message
            )
        else:
            print_log("update.message is None!")


def plot_user(
    dataset: pd.DataFrame, 
    campaign_name: str,
    query: str, 
    cache_path: str,
    chains: List[Chain],
    timeframe: str = "T"
) -> Optional[str]:
    latest_date = dataset.index.max()
    checkpoints = get_checkpoint_dates(
        campaign_name=campaign_name,
        latest_date=latest_date
    )
    lp_tokens = CAMPAIGNS.get(campaign_name, {}).get("tokens", None)

    if checkpoints is None or lp_tokens is None:
        print_log("No checkpoints found!")
        return None

    # filter user transactions
    # and only include LP tokens
    # that are included in the campaign
    user_txs = dataset[
        (dataset["user_address"] == query.lower().strip()) & \
        (dataset["token"].isin(lp_tokens))
    ]
    
    save_path = f"{cache_path}/img/{query}.png"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    #### plot user transactions ####

    if len(user_txs["token"].unique()) == 1:
        # if user have provided only 1 LP token, plot a single graph
        fig, ax = plt.subplots(1, 1, figsize=(13, 4))
        _token = user_txs["token"].unique()[0]

        # iterate through chains
        for _chain in list(
            map(Chain.resolve_connext_domain, chains)
        ):
            # get token data
            _data = dataset[
                (dataset["user_address"] == query.lower()) & \
                (dataset["chain"] == _chain) & \
                (dataset["token"] == _token)
            ]
            # if found that user has provided liquidity for this token
            if len(_data) > 0:
                # load token data
                # concatenate with 2 dummy rows to make sure
                # the data contains the starting and ending point
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
                }], index=[
                    checkpoints["start"], 
                    checkpoints["end"], 
                ])], axis=0)
                # sort index and cumsum the balance change to get the balance
                _data = _data.sort_index()
                _data = _data["balance_change"].cumsum().resample(timeframe).last().ffill()
                # filter out data before campaign start
                _data = _data[_data.index >= checkpoints["start"]]
                _data.plot(ax=ax, label=_chain)

                ax.legend()
            ax.set_title(f"{_token} Balance")
        fig.suptitle(query)

    elif len(user_txs["token"].unique()) > 1:
        # if user have provided more than 1 LP token, plot 2 graphs
        fig, ax = plt.subplots(1, 2, figsize=(13, 4))
        
        # iterate through LP tokens
        for i, _token in enumerate(lp_tokens):
            # iterate through chains
            for _chain in list(map(Chain.resolve_connext_domain, chains)):
                # get token data filtered by
                # user address, chain, and token
                _data = dataset[
                    (dataset["user_address"] == query.lower()) & \
                    (dataset["chain"] == _chain) & \
                    (dataset["token"] == _token)
                ]
                if len(_data) > 0:
                    # if found that user has provided liquidity for this token
                    # in this chain, load token data
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
                    }], index=[
                        checkpoints["start"], 
                        checkpoints["end"], 
                    ])], axis=0)
                    # sort index and cumsum the balance change to get the balance
                    _data = _data.sort_index()
                    _data = _data["balance_change"].cumsum().resample(timeframe).last().ffill()
                    _data = _data[_data.index >= checkpoints["start"]]
                    _data.plot(ax=ax[i], label=_chain)
                    ax[i].legend()
            ax[i].set_title(f"{_token} Balance")
        fig.suptitle(query)

    #### save plot ###

    fig.tight_layout()
    fig.savefig(save_path)
    return save_path


def format_campaign2s_results(wallet: str, results: dict) -> str:
    template = f"Wallet address: {wallet}\n\n"

    if "filters" in results and len(results["filters"]) > 0:
        template += f"🔫 Applied filters:\n"
        for _token, _min_value in results["filters"].items():
            if _token == Token.CWETHLP:
                template += f"    ⏩ {_min_value:.6f} {_token}\n"
            else:
                template += f"    ⏩ {_min_value:.2f} {_token}\n"

    chain_qualified = []
    for k, v in results["results"].items():
        items = k.split("_")
        token = items[-1]
        chain = " ".join(items[:-1])

        if v["is_qualified"]:
            template += f"\n🥳 You are qualified for {token} on {chain}\n"
        else:
            template += f"\n🫣 You are not qualified for {token} on {chain}\n"
            template += f"    ⏩ Reason: {v['reason']}\n"

        score = v["score"]
        if token == Token.CWETHLP:
            template += f"    ⏩ Your score is {score:.6f}\n"
        else:
            template += f"    ⏩ Your score is {score:.2f}\n"

        if v["is_qualified"]:
            chain_qualified.append(chain)

    template += f"\n⚡️ You've qualified {len(chain_qualified)} chains!\n"
    template += f"{chain_qualified}"
    return template


def format_results(wallet: str, results: dict) -> str:
    template = f"Wallet address: {wallet}\n\n"

    if "filters" in results and len(results["filters"]) > 0:
        template += f"🔫 Applied filters:\n"
        for _token, _min_value in results["filters"].items():
            if _token == Token.CWETHLP:
                template += f"    ⏩ {_min_value:.6f} {_token}\n"
            else:
                template += f"    ⏩ {_min_value:.2f} {_token}\n"

    chain_qualified = []
    for k, v in results["results"].items():
        if "LP" not in k:
            chain = k

            if v["is_qualified"]:
                template += f"\n🥳 You are qualified for {chain}\n"
            else:
                template += f"\n🫣 You are not qualified for {chain}\n"
            token = None
        else:
            items = k.split("_")
            token = items[-1]
            chain = " ".join(items[:-1])

            if v["is_qualified"]:
                template += f"\n🥳 You are qualified for {token} on {chain}\n"
            else:
                template += f"\n🫣 You are not qualified for {token} on {chain}\n"

        rank = v["rank"]
        score = v["score"]
        n_qualified = v["qualified"]
        n_participants = v["n_participants"]
        min_score = v["min_score"][-2]

        if token == Token.CWETHLP:
            template += f"    ⏩ Your score is {score:.6f} compared to the minimum score of {min_score:.6f}\n"
        else:
            template += f"    ⏩ Your score is {score:.2f} compared to the minimum score of {min_score:.2f}\n"

        template += f"    ⏩ There are a total of {n_participants} participants in this pool\n"
        template += f"    ⏩ You are at rank {rank} among {n_participants} all participants\n"
        template += f"        🦦 (at least rank {n_qualified} is required for top 30%)\n"

        if v["is_qualified"]:
            chain_qualified.append(chain)

    template += f"\n⚡️ You've qualified {len(chain_qualified)} chains!\n"
    template += f"{chain_qualified}"
    return template


def query_campaign1(
    query: str,
    user_scores: pd.DataFrame,
    chains: List[Chain],
    min_token1_value: float = 0,
    min_token2_value: float = 0,
    threshold: float = 0.3,
):
    campaign_name = "campaign_1"
    results = {
        "wallet": query
    }

    # get lp tokens associated with the campaign
    token1, token2 = CAMPAIGNS[campaign_name]["tokens"]
    
    # apply filters if needed
    filters = {}
    if min_token1_value > 0:
        print_log(f"Applying filter for with {min_token1_value} CUSDCLP")
        filters[token1] = min_token1_value
    if min_token2_value > 0:
        print_log(f"Applying filter for with {min_token2_value} CWETHLP")
        filters[token2] = min_token2_value
    results["filters"] = filters
    
    query_results = {}
    for chain, token in itertools.product(chains, [token1, token2]):
        min_value = min_token1_value if token == token1 else min_token2_value
        chain = Chain.resolve_connext_domain(chain)
        _score = user_scores[
            (user_scores["chain"] == chain) & \
            (user_scores["token"] == token)
        ].sort_values(
            "score", 
            ascending=False
        ).reset_index(drop=True)
        qualified = _score.iloc[:round(len(_score[_score["score"] > min_value]) * threshold)]
        min_score = qualified.values[-1]
        user_results = qualified[qualified["user_address"] == query]
        num_participants = len(_score)
        
        if len(user_results) > 0:
            # qualified
            query_results[f"{chain}_{token}"] = {
                "rank": user_results.index[0],
                "score": user_results["score"].values[0],
                "qualified": len(qualified),
                "n_participants": num_participants,
                "min_score": min_score,
                "is_qualified": True
            }
        elif query in _score["user_address"].values:
            # not qualified
            user_results = _score[_score["user_address"] == query]
            query_results[f"{chain}_{token}"] = {
                "rank": user_results.index[0],
                "score": user_results["score"].values[0],
                "qualified": len(qualified),
                "n_participants": num_participants,
                "min_score": min_score,
                "is_qualified": False
            }

    results["results"] = query_results
    return results


def query_campaign2(
    query: str,
    user_scores: pd.DataFrame,
    chains: List[Chain],
    min_token1_value: float = 0,
    min_token2_value: float = 0,
    threshold: float = 0.3,
):
    campaign_name = "campaign_2"
    results = {
        "wallet": query
    }

    # get lp tokens associated with the campaign
    token1, token2 = CAMPAIGNS[campaign_name]["tokens"]
    
    # apply filters if needed
    filters = {}
    if min_token1_value > 0:
        print_log(f"Applying filter for with {min_token1_value} {token1}")
        filters[token1] = min_token1_value
    if min_token2_value > 0:
        print_log(f"Applying filter for with {min_token2_value} {token2}")
        filters[token2] = min_token2_value
    results["filters"] = filters
    
    query_results = {}
    for chain in chains:
        min_value = min_token1_value + min_token2_value
        chain = Chain.resolve_connext_domain(chain)
        _score = user_scores[
            (user_scores["chain"] == chain)
        ].sort_values(
            "score", 
            ascending=False
        ).reset_index(drop=True)

        qualified = _score.iloc[:round(len(_score[_score["score"] > min_value]) * threshold)]
        min_score = qualified.values[-1]
        user_results = qualified[qualified["user_address"] == query]
        num_participants = len(_score)
        
        if len(user_results) > 0:
            # qualified
            query_results[chain] = {
                "rank": user_results.index[0],
                "score": user_results["score"].values[0],
                "qualified": len(qualified),
                "n_participants": num_participants,
                "min_score": min_score,
                "is_qualified": True
            }
        elif query in _score["user_address"].values:
            # not qualified
            user_results = _score[_score["user_address"] == query]
            query_results[chain] = {
                "rank": user_results.index[0],
                "score": user_results["score"].values[0],
                "qualified": len(qualified),
                "n_participants": num_participants,
                "min_score": min_score,
                "is_qualified": False
            }

    results["results"] = query_results
    return results


def query_campaign2s(
    query: str,
    user_scores: pd.DataFrame,
    chains: List[Chain],
    min_token1_value: float = 0,
    min_token2_value: float = 0,
    threshold: float = 0.3,
):
    results = {
        "wallet": query,
        "results": {
            _chain: {}
            for _chain in chains
        }
    }

    # get lp tokens associated with the campaign
    campaign_name = "campaign_2-special"
    token1, token2 = CAMPAIGNS[campaign_name]["tokens"]
    
    # apply filters if needed
    filters = {}
    if min_token1_value > 0:
        print_log(f"Applying filter for with {min_token1_value} {token1}")
        filters[token1] = min_token1_value
    if min_token2_value > 0:
        print_log(f"Applying filter for with {min_token2_value} {token2}")
        filters[token2] = min_token2_value
    results["filters"] = filters

    campaign1_results = query_campaign1(
        query=query,
        user_scores=user_scores,
        chains=chains,
        min_token1_value=min_token1_value,
        min_token2_value=min_token2_value,
        threshold=threshold
    )

    query_results = {}
    for key, c1_result in campaign1_results["results"].items():

        if c1_result["is_qualified"]:
            # if qualified for campaign 1
            *chain, token = key.split("_")
            chain = "_".join(chain)
            
            _score = user_scores[
                (user_scores["chain"] == chain) & \
                (user_scores["token"] == token)
            ].sort_values(
                "score", 
                ascending=False
            ).reset_index(drop=True)
            special_threshold = 100 if token == Token.CUSDCLP else 0.1
            qualified = _score[_score["score"] > special_threshold]
            user_results = qualified[qualified["user_address"] == query]
            
            if len(user_results) > 0:
                # qualified
                query_results[f"{chain}_{token}"] = {
                    "score": user_results["score"].values[0],
                    "is_qualified": True
                }
            elif query in _score["user_address"].values:
                # not qualified
                user_results = _score[_score["user_address"] == query]
                query_results[f"{chain}_{token}"] = {
                    "score": user_results["score"].values[0],
                    "is_qualified": False,
                    "reason": f"Holdings {token} less than {special_threshold} {token}"
                }
        else:
            _score = user_scores[
                (user_scores["chain"] == chain) & \
                (user_scores["token"] == token)
            ].sort_values(
                "score", 
                ascending=False
            ).reset_index(drop=True)
            query_results[key] = {
                "score": c1_result["score"],
                "is_qualified": False,
                "reason": f"Did not qualify for campaign 1"
            }

    results["results"] = query_results
    return results


def query_user(
    query: str, 
    campaign_name: str,
    user_scores: Optional[pd.DataFrame],
    chains: List[Chain],
    min_token1_value: float = 0, 
    min_token2_value: float = 0,
    threshold: float = 0.3
) -> None:
    # initialize results
    query = query.lower().strip()\
        .replace("<", "").replace(">", "")\
        .replace("[", "").replace("]", "")
    
    if campaign_name == "campaign_1":
        results = query_campaign1(
            query=query,
            user_scores=user_scores,
            chains=chains,
            min_token1_value=min_token1_value,
            min_token2_value=min_token2_value,
            threshold=threshold
        )
    elif campaign_name == "campaign_2":
        results = query_campaign2(
            query=query,
            user_scores=user_scores,
            chains=chains,
            min_token1_value=min_token1_value,
            min_token2_value=min_token2_value,
            threshold=threshold
        )
    elif campaign_name == "campaign_2-special":
        results = query_campaign2s(
            query=query,
            user_scores=user_scores,
            chains=chains,
            min_token1_value=min_token1_value,
            min_token2_value=min_token2_value,
            threshold=threshold
        )
    else:
        raise ValueError(f"Invalid campaign name: {campaign_name}")
    
    return {
        "statusCode": 200,
        "body": results
    }
    