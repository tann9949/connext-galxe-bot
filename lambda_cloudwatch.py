import json
import os
from datetime import datetime, timedelta

import boto3

client = boto3.client("sqs")
OFFSET = 1
WINDOW = 5
CHAINS = [
    1869640809,
    1634886255,
    6450786,
    6778479,
    1886350457,
]
QUEUES = [
    os.getenv("SQS_TRANSACTIONS_URL"),
    os.getenv("SQS_TRANSFERS_URL"),
]


def lambda_handler(event, context):
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=WINDOW+OFFSET)

    for queue_url in QUEUES:
        entries = []
        if queue_url is None:
            continue
        for chain in CHAINS:
            st = start_time.strftime("%Y-%m-%dT%H:%M:%S")
            et = end_time.strftime("%Y-%m-%dT%H:%M:%S")
            msg_id = f"{chain}-{st}-{et}".replace(":", "-")
            print(f"Sending message to {os.path.basename(queue_url)} for {chain} from {st} to {et}")
            payload = {
                "chain": chain,
                "start_datetime": st,
                "end_datetime": et,
            }
            entries.append({
                "Id": msg_id,
                "MessageBody": json.dumps(payload),
                "MessageGroupId": "connext-lp-scheduler"
            })

        client.send_message_batch(
            QueueUrl=queue_url,
            Entries=entries,
        )
