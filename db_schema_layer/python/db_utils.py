from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker

Session = None


def create_db_engine(db_conn: str, debug_mode: bool = False) -> Engine:
    return create_engine(
        db_conn,
        echo=debug_mode,
        pool_size=10,
        max_overflow=20,
        pool_recycle=3600,
        pool_pre_ping=True,
        pool_use_lifo=True,
    )


def create_session(engine):
    global Session
    if Session is None:
        Session = sessionmaker(bind=engine)
    return Session()
