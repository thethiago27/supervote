from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from db_schema_layer.user.user_schema import User

Base = declarative_base()


def create_db_schema(engine):
    Base.metadata.create_all(engine)


class Poll(Base):
    __tabename__ = 'poll'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey('user.id'))
    create_at = Column(DateTime)
    expire_at = Column(DateTime)

    owner = relationship(User, backref="polls")
    poll_options = relationship("PollOption", backref="poll")

    def __repr__(self):
        return f"<Poll(name={self.name}, poll_owner={self.poll_owner}, created_at={self.created_at}, expire_at={self.expire_at})>"

    def __init__(self, name, poll_owner, created_at, expire_at):
        self.name = name
        self.poll_owner = poll_owner
        self.created_at = created_at
        self.expire_at = expire_at
