import json
import logging
from typing import Dict, List, Optional

import db_connection
from poll_schema import Poll, Base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

session = db_connection.get_db_connection()
engine = db_connection.create_db_session(session)
Base.metadata.create_all(engine)


def get_poll_by_id(poll_id: int) -> Optional[Poll]:
    return session.query(Poll).filter(Poll.id == poll_id).first()


# def get_poll_options_by_poll_id(poll_id: int) -> List[PollOptions]:
#     return session.query(PollOptions).filter(PollOptions.poll_id == poll_id).all()


@db_connection.db_session
def lambda_handler(event: Dict, context: Dict) -> Dict:
    poll_id = event.get('poll-id')
    if not poll_id:
        logger.info("Missing 'poll-id' in event data")
        return {'statusCode': 400, 'body': "Missing 'poll_id' in request data"}

    poll = get_poll_by_id(poll_id)
    if not poll:
        logger.info(f"Poll with id {poll_id} not found")
        return {'statusCode': 404, 'body': f"Poll with id {poll_id} not found"}

    # poll_options = get_poll_options_by_poll_id(poll_id)
    logger.info(f"Poll found successfully: {poll}")

    response = {
        'statusCode': 200,
        'body': json.dumps({
            'poll': poll.to_dict(),
        })
    }

    return response


def main():
    try:
        event = {...}  # Replace with your event data
        context = {...}  # Replace with your context data
        response = lambda_handler(event, context)
        print(response)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        return {'statusCode': 500, 'body': "Internal server error"}


if __name__ == '__main__':
    main()
