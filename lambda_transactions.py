import json
from datetime import datetime

from src.process_queue import process_transaction


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
    
    print(f"Message: {message_id}")
    print(f"Start: {start_datetime}")
    print(f"End: {end_datetime}")
    print(f"Chain: {chain}")

    try:
        process_transaction(record)
    except Exception as e:
        print(e)
        raise e

    return {
        'statusCode': 200,
        'body': json.dumps('Queue process successful!')
    }
