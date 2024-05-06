import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


def create_db_schema(engine):
    Base.metadata.create_all(engine)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    is_active = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    poll_votes = relationship("PollVote", backref="user")

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email}, is_active={self.is_active}, password={self.password})>"

    def __init__(self, email, password, name, is_active):
        self.is_active = is_active
        self.email = email
        self.password = password
        self.name = name
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
