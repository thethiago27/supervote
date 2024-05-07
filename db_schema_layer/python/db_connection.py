import json
import logging
import os
from typing import Dict, Union, Any

import boto3
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

rds_client = boto3.client('rds')
secrets_manager_client = boto3.client('secretsmanager')


def get_secrets(secret_name: str) -> Dict:
    response = secrets_manager_client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])


def get_db_password(db_endpoint: str, secrets: Dict) -> str:
    response = rds_client.generate_db_auth_token(
        DBHostname=db_endpoint,
        Port=secrets['port'],
        DBUsername=secrets['username'],
    )
    return response['AuthToken']


def create_db_engine(db_endpoint: str, secrets: Dict) -> Engine:
    password = get_db_password(db_endpoint, secrets)
    conn_string = f"postgresql://{secrets['username']}:{password}@{db_endpoint}:{secrets['port']}/{secrets['dbname']}?sslmode=require"
    return create_engine(conn_string)


def create_session_factory(engine: Engine) -> scoped_session[Union[Session, Any]]:
    return scoped_session(sessionmaker(bind=engine))


def get_db_session() -> sessionmaker:
    db_endpoint = os.getenv('DB_ENDPOINT')
    db_secret_name = os.getenv('DB_SECRET_NAME')

    if not db_endpoint or not db_secret_name:
        logger.error("Missing required environment variables: DB_ENDPOINT or DB_SECRET_NAME")
        raise ValueError("Missing required environment variables")

    secrets = get_secrets(db_secret_name)
    engine = create_db_engine(db_endpoint, secrets)
    session_factory = create_session_factory(engine)

    return session_factory
