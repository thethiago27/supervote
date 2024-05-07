import json
import logging
import os
from typing import Dict

import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('votes')
sqs = boto3.client('sqs')


def check_has_user_voted(user_id: str, poll_id: str) -> bool:
    response = table.get_item(Key={'user_id': user_id, 'poll_id': poll_id})
    return 'Item' in response


def send_vote_to_queue(user_id: str, poll_id: str) -> Dict:
    message = {
        'user_id': user_id,
        'poll_id': poll_id
    }

    queue_url = os.getenv('VOTE_QUEUE_URL')
    if not queue_url:
        logger.error("VOTE_QUEUE_URL environment variable not set")
        return {'statusCode': 500, 'body': "Internal server error"}

    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message)
    )

    logger.info(f"Vote registered successfully: {response}")
    return {'statusCode': 201, 'body': ''}


def lambda_handler(event: Dict, context: Dict) -> Dict:
    user_id = event.get('principalId')
    poll_id = event.get('poll_id')

    if not user_id or not poll_id:
        logger.info("Missing 'principalId' or 'poll_id' in event data")
        return {'statusCode': 400, 'body': "Missing required parameters"}

    if check_has_user_voted(user_id, poll_id):
        return {'statusCode': 400, 'body': json.dumps({'message': 'User has already voted'})}

    return send_vote_to_queue(user_id, poll_id)
