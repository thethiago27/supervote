import json
import logging
import os

import boto3

from db_utils import create_db_session

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DB_ENDPOINT = os.getenv('DB_ENDPOINT')
DB_SECRET_NAME = os.getenv('DB_SECRET_NAME')

session = boto3.Session(profile_name='default')
client = session.client('rds')
secrets_client = session.client('secretsmanager')


def get_secrets():
    secret_response = secrets_client.get_secret_value(SecretId=DB_SECRET_NAME)
    secrets = json.loads(secret_response['SecretString'])
    return secrets


def get_db_password():
    secrets = get_secrets()
    response = client.generate_db_auth_token(
        DBHostname=DB_ENDPOINT,
        Port=secrets['port'],
        DBUsername=secrets['username'],
    )
    return response


def get_db_connection():
    secrets = get_secrets()
    password = get_db_password()
    conn = f"postgresql://{secrets['username']}:{password}@{DB_ENDPOINT}:{secrets['port']}/{secrets['dbname']}?sslmode=require"

    logger.info(f"Connecting to DB: {conn}")
    engine = create_db_session(conn)
    db_session = create_db_session(engine)

    return db_session
