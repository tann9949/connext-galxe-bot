import os
import sys

sys.path.append(os.getcwd())


import multiprocessing as mp
from argparse import ArgumentParser, Namespace
from datetime import datetime, timedelta
from functools import partial

from dotenv import load_dotenv

from src.process_queue import process_transaction, process_transfers

if load_dotenv():
    print("Loaded .env file")
else:
    print("No .env file found")
    sys.exit(1)


def run_parser() -> Namespace:
    """Parse command line arguments"""
    parser = ArgumentParser(
        description="Run historical transactions/transfers for Connext LP analysis",
        epilog="Example: python run_historical_transactions.py --start_datetime=2021-01-01T00:00:00Z --end_datetime=2021-01-01T00:00:00Z --time_window=5 --num_jobs=10",
    )
    parser.add_argument(
        "--chain",
        type=str,
        required=True,
        help="Chain to run on (polygon, optimism, arbitrum, bsc, gnosis)",
    )
    parser.add_argument(
        "--start_datetime",
        type=str,
        default="2022-12-21T00:00:00",
        help="Start datetime in ISO format",
    )
    parser.add_argument(
        "--end_datetime",
        type=str,
        default="2023-04-17T00:00:00",  # currently up to 2023-04-19T14:00:00
        help="End datetime in ISO format",
    )
    parser.add_argument(
        "--time_window",
        type=int,
        default=24,
        help="Time window in hours",
    )
    parser.add_argument(
        "--num_jobs",
        type=int,
        default=os.cpu_count(),
        help="Number of jobs to flood the queue with",
    )
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Offset in minutes",
    )
    parser.add_argument(
        "--exist_check",
        action="store_true",
        help="Check if the file exists before processing before inserting to the database. This is useful if you want to resume a previous run, but make your run slower",
    )
    return parser.parse_args()


def get_queue_items(
    chain: str, start_datetime: str, end_datetime: str, 
    time_window: int, offset: int = 0) -> list:
    """Get a list of time ranges and chain"""
    if chain == "gnosis":
        chain = 6778479
    elif chain == "bsc":
        chain = 6450786
    elif chain == "arbitrum":
        chain = 1634886255
    elif chain == "optimism":
        chain = 1869640809
    elif chain == "polygon":
        chain = 1886350457
    else:
        raise ValueError(f"Invalid chain: {chain}")

    st = datetime.fromisoformat(start_datetime)
    et = datetime.fromisoformat(end_datetime)

    queue_items = []
    while st < et:
        end_batch = st + timedelta(hours=time_window+offset) if st + timedelta(hours=time_window) < et else et
        queue_items.append({
            "start_datetime": st.isoformat(), 
            "end_datetime": end_batch.isoformat(),
            "chain": chain,
        })
        st = end_batch
    
    return queue_items


def main(args: Namespace) -> None:
    """Main function"""
    queue_items = get_queue_items(
        chain=args.chain,
        start_datetime=args.start_datetime,
        end_datetime=args.end_datetime,
        time_window=args.time_window,
        offset=args.offset,
    )
    print(f"Get total of {len(queue_items)} items to process")

    n_workers = min(args.num_jobs, len(queue_items))
    print("Processing transactions")
    with mp.Pool(processes=n_workers) as pool:
        pool.map(
            partial(process_transaction, exist_check=args.exist_check), 
            queue_items)
    print("Done processing transactions")

    print("Processing transfers")
    with mp.Pool(processes=n_workers) as pool:
        pool.map(
            partial(process_transfers, exist_check=args.exist_check),
            queue_items)
    print("Done processing transfers")


if __name__ == "__main__":
    args = run_parser()
    main(args)
