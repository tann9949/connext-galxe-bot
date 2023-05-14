from datetime import datetime
from typing import Dict, Optional

from src.erc20 import Token
from src.utils import print_log


CAMPAIGNS = {
    # https://galxe.com/connextnetwork/campaign/GC1SiU4gvJ
    "campaign_1": {
        "tokens": [Token.CUSDCLP, Token.CWETHLP],
        "sybil_check": [Token.USDC, Token.WETH],
        # 15 Feb 2023 00:00:00 UTC
        "start": datetime.fromtimestamp(1676419200),
        # 15 May 2023 00:00:00 UTC
        "end": datetime.fromtimestamp(1684108800),
    },
    # https://galxe.com/connextnetwork/campaign/GCEtNUya7s
    "campaign_2-special": {
        "tokens": [Token.CUSDCLP, Token.CWETHLP],
        # 09 May 2023 00:00:00 UTC
        "start": datetime.fromtimestamp(1683590400),
        # 23 June 2023 00:00:00 UTC
        "end": datetime.fromtimestamp(1687478400),
    },
    "campaign_2": {
        "tokens": [Token.CUSDTLP, Token.CDAILP],
        "sybil_check": [Token.USDT, Token.DAI],
        # 09 May 2023 00:00:00 UTC
        "start": datetime.fromtimestamp(1683590400),
        # 23 June 2023 00:00:00 UTC
        "end": datetime.fromtimestamp(1687478400),
    }
}


def get_checkpoint_dates(campaign_name: str, latest_date: datetime) -> Optional[Dict[str, datetime]]:
    """Get checkpoint dates for a campaign
    """
    checkpoint_dates = {}
    campaign = CAMPAIGNS.get(campaign_name, None)

    if campaign is None:
        print_log(f"Campaign {campaign_name} not found")
        return None

    if campaign["start"] is None or campaign["end"] is None:
        # campaign has not started or ended
        print_log(f"Campaign {campaign_name} has not started or ended")
        return None

    if latest_date > campaign["end"]:
        # campaign has ended
        print_log(f"Campaign {campaign_name} has ended, using end date as checkpoint")
        checkpoint_dates["end"] = campaign["end"]
    else:
        # campaign is still running
        print_log(f"Campaign {campaign_name} is still running, using latest date as checkpoint")
        checkpoint_dates["end"] = latest_date

    if latest_date > campaign["start"]:
        # campaign has started
        checkpoint_dates["start"] = campaign["start"]
    else:
        # campaign has not started
        print_log(f"Campaign {campaign_name} has not started, skipping...")
        return None
    return checkpoint_dates