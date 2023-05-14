from __future__ import annotations

import os
from datetime import datetime
from functools import partial
from typing import List, Optional

import pandas as pd
from telegram import Update
from telegram.ext import (Application, CallbackContext, CommandHandler,
                          MessageHandler, filters)

from src.bot.utils import (format_campaign2s_results, format_results,
                           plot_user, query_user, reply_image, reply_markdown,
                           reply_message)
from src.campaign import CAMPAIGNS
from src.constant import Chain
from src.utils import print_log


class ConnextTelegramBot(object):

    def __init__(
        self, 
        cache_path: str,
        log_path: Optional[str] = None,
        chains: Optional[List[Chain]] = None
    ) -> None:
        self.cache_path = cache_path
        self.log_path = log_path
        self.chains = [
            Chain.ARBITRUM_ONE,
            Chain.BNB_CHAIN,
            Chain.OPTIMISM,
            Chain.GNOSIS,
            Chain.POLYGON
        ] if chains is None else chains
        self.app = Application.builder().token(
            token=os.getenv("TELEGRAM_BOT_TOKEN")
        ).build()
        self.campaigns = {
            "campaign1": "campaign_1",
            "campaign2": "campaign_2",
            "special": "campaign_2-special",
        }
        self.add_default_handler()
        self.add_command_handler("start", ConnextTelegramBot.start_callback)
        self.add_command_handler("help", ConnextTelegramBot.start_callback)
        self.add_command_handler("calculation", ConnextTelegramBot.calculation_callback)
        self.add_command_handler("source", ConnextTelegramBot.source_callback)

        for campaign_cmd, _campaign in self.campaigns.items():
            print(f"Adding handlers for {campaign_cmd}_stats")
            self.add_command_handler(
                f"{campaign_cmd}_stats", 
                partial(
                    ConnextTelegramBot.stats_callback,
                    campaign_name=_campaign,
                    bot=self))
            print(f"Adding handlers for {campaign_cmd}_score")
            self.add_command_handler(
                f"{campaign_cmd}_score", 
                partial(
                    ConnextTelegramBot.score_callback,
                    campaign_name=_campaign,
                    bot=self))
            
            if _campaign != "campaign_2-special":
                print(f"Adding handlers for {campaign_cmd}_score_filter")
                self.add_command_handler(
                    f"{campaign_cmd}_score_filter", 
                    partial(
                        ConnextTelegramBot.score_filter_callback,
                        campaign_name=_campaign,
                        bot=self))

    #### bot utility functions ####

    @staticmethod
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

    def load_cache(self, campaign_name: str) -> pd.DataFrame:
        dataset = []
        for chain in self.chains:
            df = pd.read_csv(
                f"{self.cache_path}/{campaign_name}/{Chain.resolve_connext_domain(chain)}_user_scores.csv"
            )
            df["chain"] = Chain.resolve_connext_domain(chain)
            dataset.append(df)
        return pd.concat(dataset, axis=0).reset_index(drop=True)
    
    def load_dataset(self):
        df = pd.read_csv(f"{self.cache_path}/full_dataset.csv")
        df["datetime"] = df["datetime"].map(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
        df = df.set_index("datetime").sort_index()
        return df
    
    #### bot callback functions ####

    async def start_callback(update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        print_log(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Default callback triggered")
        await reply_markdown(update,
            "👾 Welcome to the Unofficial Connext Galxe Bot\!\n"
            "The bot🤖 was **created by Connext Contributor** \(not the team\!\) to facilitate the LP Rewards campaign\n\n"
            "To use the bot, you can use the following commands👇:\n"
            "`/campaign1_score <wallet>` \- Get your score for the [1st Galxe Campaign](https://galxe.com/connextnetwork/campaign/GC1SiU4gvJ)\n"
            "`/campaign1_score_filter <wallet> <token>` \- Get your score with filters applied for the [1st Galxe Campaign](https://galxe.com/connextnetwork/campaign/GC1SiU4gvJ)\n"
            "`/campaign1_stats <wallet>` \- Get your historical LP stats for the [1st Galxe Campaign](https://galxe.com/connextnetwork/campaign/GC1SiU4gvJ)\n"
            "`/campaign2_score <wallet>` \- Get your score for the [2nd Galxe Campaign](https://galxe.com/connextnetwork/campaign/GCEtNUya7s)\n"
            "`/campaign2_score_filter <wallet> <token>` \- Get your score with filters applied for the [2nd Galxe Campaign](https://galxe.com/connextnetwork/campaign/GCEtNUya7s)\n"
            "`/campaign2_stats <wallet>` \- Get your historical LP stats for the [2nd Galxe Campaign](https://galxe.com/connextnetwork/campaign/GCEtNUya7s)\n"
            "`/special_score <wallet>` \- Get your score for the [Special Galxe Campaign](https://galxe.com/connextnetwork/campaign/GCHhsUEEYn)\n"
            "`/special_stats <wallet>` \- Get your historical LP stats for the [Special Galxe Campaign](https://galxe.com/connextnetwork/campaign/GCHhsUEEYn)\n"
            "`/source` \- Get the source code of this project\n"
            "`/calculation` \- Understand how scores are calculated\n"
            "`/help` or `/start` \- Get help on how to use the bot\n\n"
            "🚨 Note that the results showed by this bot **is consider not a final decision** \!\n"
            "❗️ **The final decision will be made by the Connext team after sybil filtering was applied\!**")
        
    @staticmethod
    async def source_callback(update: Update, context: CallbackContext) -> None:
        """Return string specifying source code"""
        print_log(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Source code callback triggered")
        await reply_markdown(update,
            "🤖💻🔧 **Bot Source Code**\n"
            "The source code of this project can be found [here](https://github.com/tann9949/connext-galxe-bot/)\n\n"
            "If you want to report any bugs, feels free to report it to `@chompk.eth` in [Connext Discord](https://discord.gg/connext)")
        
    @staticmethod
    async def calculation_callback(update: Update, context: CallbackContext) -> None:
        """Return string specifying calculation method"""
        print_log(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Calculation callback triggered")
        await reply_markdown(update,
            "📟 **Score calculation Guide**\n\n"
            "The score is calculated using the time\-weighted average"
            "LP position where the timeframe for averaging is 1 minute\."
            "\n\n"
            "The score are then sorted and top 30\% are considered qualified\."
            "\n\n"
            "If there's any filter applied, any position that have an average"
            "LP position with less than specified will be removed\. Causing the"
            "number of top 30\% to be further reduced\.\n\n")
        
    @staticmethod
    async def stats_callback(update: Update, context: CallbackContext, campaign_name: str, bot: ConnextTelegramBot) -> None:
        """Plot user LP balance across all assets for all chains"""
        curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # get arguments
        args = context.args
        if len(args) != 1:
            await reply_message(update,
                        f"Please add your wallet as an argument!\ne.g. /campaign1_stats <wallet>")
            return
        wallet = args[0].lower().strip()\
            .replace("<", "").replace(">", "")\
            .replace("[", "").replace("]", "")
        
        print_log(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Getting stats {wallet}")
        fig_path = plot_user(
            dataset=bot.load_dataset(),
            campaign_name=campaign_name,
            query=wallet,
            cache_path=bot.cache_path,
            chains=bot.chains
        )

        with open(bot.log_path, "a") as fp:
            fp.write(f"{curr_time},stats\n")

        if not os.path.exists(fig_path):
            await reply_message(update, "🤔 You haven't participate in this campaign!")
        else:
            await reply_image(
                update,
                fig_path
            )
            os.remove(fig_path)

    @staticmethod
    async def score_callback(update: Update, context: CallbackContext, campaign_name: str, bot: ConnextTelegramBot) -> None:
        """Calculate score, average LP holdings by minutes, of a user in
        a given campaign
        """
        curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # get arguments
        args = context.args
        if len(args) != 1:
            await reply_message(
                update,
                f"Please add your wallet as an argument!\ne.g. /campaign1_score 0x1234...5678")
            return
        wallet = args[0].lower().strip()\
            .replace("<", "").replace(">", "")\
            .replace("[", "").replace("]", "")
        
        print_log(f"[{curr_time}] Querying {wallet}")
        results = query_user(
            query=wallet, 
            campaign_name=campaign_name,
            bot=bot,
            chains=bot.chains)
        
        if campaign_name == "campaign_2-special":
            template = format_campaign2s_results(wallet, results["body"])
        else:
            template = format_results(wallet, results["body"])

        with open(bot.log_path, "a") as fp:
            fp.write(f"{curr_time},score\n")
        await reply_message(
            update,
            template
        )

    @staticmethod
    async def score_filter_callback(
        update: Update, 
        context: CallbackContext, 
        campaign_name: str, 
        bot: ConnextTelegramBot) -> None:
        """Calculate score, average LP holdings by minutes, of a user in
        a given campaign with filters applied.
        """
        curr_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # load args
        token1, token2 = CAMPAIGNS[campaign_name]["tokens"]
        args = context.args
        if len(args) != 3:
            await reply_message(
                update,
                f"Please add your wallet and minimum {token1}/{token2} "
                f"filter as an argument!\ne.g. "
                f"/{campaign_name}score_filter <min-{token1}> <min-{token2}> <wallet>")
            return
        
        # get arguments
        # parse arguments from string to float
        try:
            min_tok1 = float(args[0].strip())
        except ValueError:
            await reply_message(update,
                        f"<min-{token1}> must be in a float (numerical) format! {args}")
            return
        
        try:
            min_tok2 = float(args[1].strip())
        except ValueError:
            await reply_message(update,
                        f"<min-{token2}> must be in a float (numerical) format {args}")
            return
        # parse wallet
        wallet = args[2].lower().strip()\
            .replace("<", "").replace(">", "")\
            .replace("[", "").replace("]", "")
        
        print_log(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"Querying {wallet}, "
            f"fillter {min_tok1} {token1}, {min_tok2} {token2}")
        results = query_user(
            query=wallet, 
            campaign_name=campaign_name,
            user_scores=bot.load_cache(campaign_name=campaign_name), 
            chains=bot.chains,
            min_token1_value=min_tok1,
            min_token2_value=min_tok2)
        template = format_results(wallet, results["body"])

        with open(bot.log_path, "a") as fp:
            fp.write(f"{curr_time},score_filter\n")
        await reply_message(
            update,
            template
        )

    #### bot functions ####

    def add_command_handler(
        self,
        command: str,
        callback: callable
    ) -> None:
        self.app.add_handler(
            CommandHandler(
                command=command,
                callback=callback
            )
        )

    def add_default_handler(
        self,
    ) -> None:
        self.app.add_handler(
            MessageHandler(
                filters=filters.TEXT & ~filters.COMMAND,
                callback=ConnextTelegramBot.start_callback
            )
        )

    def run(self) -> None:
        print_log("Bot started!")
        self.app.run_polling()
    