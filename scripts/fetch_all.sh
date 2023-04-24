#!/bin/bash

# args
start_datetime=$1
end_datetime=$2
time_window=$3

# default
if [ -z "$start_datetime" ]; then
  start_datetime="2022-12-21T00:00:00"
fi

if [ -z "$end_datetime" ]; then
  end_datetime="2023-04-20T00:00:00"
fi

if [ -z "$time_window" ]; then
  time_window=120  # 5 days
fi

for chain in gnosis bsc optimism polygon arbitrum; do
  echo "Fetching $chain"
  echo "python scripts/run_historical_transactions.py --chain=$chain --start_datetime=$start_datetime --end_datetime=$end_datetime --time_window=$time_window --exist_check"
  python scripts/run_historical_transactions.py --chain=$chain --start_datetime=$start_datetime --end_datetime=$end_datetime --time_window=$time_window --exist_check
done
