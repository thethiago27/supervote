from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from db_schema_layer.poll.poll_schema import Poll

Base = declarative_base()


def create_db_schema(engine):
    Base.metadata.create_all(engine)


class PollOptions(Base):
    __tablename__ = 'poll_option'

    id = Column(Integer, primary_key=True)
    poll_id = Column(Integer, ForeignKey('poll.id'))
    name = Column(String)

    poll = relationship(Poll, backref="poll_options")
    poll_votes = relationship("PollVote", backref="poll_option")

    def __repr__(self):
        return f"<PollOption(name={self.name}, poll_id={self.poll_id})>"

    def __init__(self, poll_id, name):
        self.poll_id = poll_id
        self.name = name