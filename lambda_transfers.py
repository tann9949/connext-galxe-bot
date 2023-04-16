import json
from datetime import datetime

from src.process_queue import process_transfers
from src.utils import print_log


def lambda_handler(event, context):
    queue_records = event.get("Records")
    assert len(queue_records) == 1
    record = json.loads(queue_records[0]["body"])
    message_id = queue_records[0].get("messageId")
    
    chain = record.get("chain")
    start_datetime = datetime.strptime(
        record.get("start_datetime"),
        "%Y-%m-%dT%H:%M:%S"
    )
    end_datetime = datetime.strptime(
        record.get("end_datetime"),
        "%Y-%m-%dT%H:%M:%S"
    )
    
    print_log(f"Message: {message_id}")
    print_log(f"Start: {start_datetime}")
    print_log(f"End: {end_datetime}")
    print_log(f"Chain: {chain}")

    try:
        process_transfers(record)
    except Exception as e:
        print_log(e)
        raise e

    return {
        'statusCode': 200,
        'body': json.dumps('Queue process successful!')
    }
