import logging
import os
from typing import Dict, Optional
import jwt

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_authorization_header(event: Dict) -> Optional[str]:
    headers = event.get('headers')
    if headers:
        return headers.get('authorization')
    return None


def decode_token(token: str) -> Optional[Dict]:
    try:
        jwt_secret = os.getenv('jwt_secret')
        if jwt_secret:
            return jwt.decode(token, jwt_secret, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        logger.info("Token expired")
    except jwt.InvalidTokenError:
        logger.error("Invalid token")
    return None


def generate_policy(principal_id: str, effect: str, method_arn: str) -> Dict:
    policy = {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': method_arn
            }]
        }
    }
    return policy


def lambda_handler(event: Dict, context: Dict) -> Dict:
    logger.info(event)
    authorization_header = get_authorization_header(event)

    if not authorization_header:
        logger.info("Authorization header not found", event)
        return generate_policy('user', 'Deny', event['methodArn'])

    token = authorization_header.split(' ')[1]
    decoded_token = decode_token(token)

    if decoded_token and 'user_id' in decoded_token:
        logger.info("User ID found in token")
        return generate_policy(decoded_token['user_id'], 'Allow', event['methodArn'])
    else:
        logger.info("User ID not found in token")
        return generate_policy('user', 'Deny', event['methodArn'])
