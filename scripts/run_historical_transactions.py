import os
import sys
sys.path.append(os.getcwd())


import multiprocessing as mp
from argparse import ArgumentParser, Namespace
from datetime import datetime, timedelta

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
        "--start_datetime",
        type=str,
        default="2022-11-01T00:00:00",
        help="Start datetime in ISO format",
    )
    parser.add_argument(
        "--end_datetime",
        type=str,
        default="2023-04-16T12:00:00",
        help="End datetime in ISO format",
    )
    parser.add_argument(
        "--time_window",
        type=int,
        default=5,
        help="Time window in minutes",
    )
    parser.add_argument(
        "--num_jobs",
        type=int,
        default=os.cpu_count() - 3,
        help="Number of jobs to flood the queue with",
    )
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Offset in minutes",
    )
    return parser.parse_args()


def get_queue_items(start_datetime: str, end_datetime: str, time_window: int, offset: int = 0) -> list:
    """Get a list of time ranges and chain"""
    st = datetime.fromisoformat(start_datetime)
    et = datetime.fromisoformat(end_datetime)

    queue_items = []
    while st < et:
        for chain in [
            1886350457, 
            1634886255, 
            1869640809, 
            6778479, 
            6450786
        ]:
            queue_items.append({
                "start_datetime": st.isoformat(), 
                "end_datetime": (st + timedelta(minutes=time_window+offset)).isoformat(),
                "chain": chain,
            })
        st += timedelta(minutes=time_window)
    
    return queue_items


def main(args: Namespace) -> None:
    """Main function"""
    queue_items = get_queue_items(
        start_datetime=args.start_datetime,
        end_datetime=args.end_datetime,
        time_window=args.time_window,
        offset=args.offset,
    )

    print("Processing transactions")
    with mp.Pool(processes=args.num_jobs) as pool:
        pool.map(process_transaction, queue_items)
    print("Done processing transactions")

    print("Processing transfers")
    with mp.Pool(processes=args.num_jobs) as pool:
        pool.map(process_transfers, queue_items)
    print("Done processing transfers")


if __name__ == "__main__":
    args = run_parser()
    main(args)
