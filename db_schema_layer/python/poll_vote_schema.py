from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from db_schema_layer.python.poll_options_schema import PollOptions
from db_schema_layer.python.poll_schema import Poll
from db_schema_layer.python.user_schema import User

Base = declarative_base()


def create_db_schema(engine):
    Base.metadata.create_all(engine)


class PollVote(Base):
    __tablename__ = 'poll_vote'

    id = Column(Integer, primary_key=True)
    poll_id = Column(Integer, ForeignKey('poll.id'))
    poll_option_id = Column(Integer, ForeignKey('poll_option.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    poll = relationship(Poll, backref="poll_votes")
    poll_option = relationship(PollOptions, backref="poll_votes")
    user = relationship(User, backref="poll_votes")

    def __repr__(self):
        return f"<PollVote(poll_id={self.poll_id}, poll_option_id={self.poll_option_id}, user_id={self.user_id})>"
