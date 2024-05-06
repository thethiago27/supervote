import json
import logging
import os

import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('votes')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

sqs = boto3.client('sqs')


def check_has_user_voted(user_id, poll_id):
    response = table.get_item(Key={'user_id': user_id, 'poll_id': poll_id})
    return 'Item' in response


def lambda_handler(event, context):
    user_id = event['principalId']
    poll_id = event['poll_id']

    if check_has_user_voted(user_id, poll_id):
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'User has already voted'})
        }

    message = {
        'user_id': user_id,
        'poll_id': poll_id
    }

    response = sqs.send_message(
        QueueUrl=os.getenv('VOTE_QUEUE_URL'),
        MessageBody=json.dumps(message)
    )

    logger.info(f"Vote registered successfully: {response}")

    return {
        'statusCode': 201,
        'body': ''
    }


