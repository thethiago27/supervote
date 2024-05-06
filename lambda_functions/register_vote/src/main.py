import json
import logging
from datetime import datetime

import boto3
from db_schema_layer import db_connection
from db_schema_layer.poll.poll_vote_schema import PollVote

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

session = db_connection.get_db_connection()
engine = db_connection.create_db_session(session)

sqs = boto3.client('sqs')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('votes')


def register_vote(poll_id, poll_option_id, user_id):
    poll_vote = PollVote(poll_id=poll_id, poll_option_id=poll_option_id, user_id=user_id)
    session.add(poll_vote)
    session.commit()

    return poll_vote


def lambda_handler(event, context):
    for record in event['Records']:
        message = json.loads(record['body'])
        receipt_handle = record['receiptHandle']
        poll_id = message['poll_id']
        poll_option_id = message['poll_option_id']
        user_id = message['user_id']

        register_vote(poll_id, poll_option_id, user_id)

        table.put_item(
            Item={
                'poll_id': poll_id,
                'user_id': user_id,
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )

        sqs.delete_message(
            QueueUrl=record['eventSourceARN'],
            ReceiptHandle=receipt_handle['receiptHandle']
        )
