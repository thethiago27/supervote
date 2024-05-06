import json
import logging
import db_connection
from poll_options_schema import PollOptions
from poll_schema import Poll

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

session = db_connection.get_db_connection()
engine = db_connection.create_db_session(session)


def get_poll_by_id(poll_id):
    poll = session.query(Poll).filter(Poll.id == poll_id).first()
    return poll


def get_poll_options_by_poll_id(poll_id):
    poll_options = session.query(PollOptions).filter(PollOptions.poll_id == poll_id).all()
    return poll_options


def lambda_handler(event, context):
    try:
        poll_id = event.get('poll-id')
        poll = get_poll_by_id(poll_id)

        if not poll_id:
            logger.info("Missing 'poll-id' in event data")
            return {
                'statusCode': 400,
                'body': "Missing 'poll_id' in request data"
            }

        if not poll:
            logger.info(f"Poll with id {poll_id} not found")
            return {
                'statusCode': 404,
                'body': f"Poll with id {poll_id} not found"
            }

        poll_options = get_poll_options_by_poll_id(poll_id)

        logger.info(f"Poll found successfully: {poll}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'poll': poll.__dict__,
                'poll_options': [poll_option.__dict__ for poll_option in poll_options]
            })
        }

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': "Internal server error"
        }

