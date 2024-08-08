# TODO create general DB interface to work with any DB
# TODO move sqlite code to slite class that expands DB interface

"""
This modul describes a SQLite(!) DB connection
and create db file with tables, allows to create a connection.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

DB_SESSION: Session | None = None


def get_session():
    """
    Creates or returns existing DB session.
    :return: db session
    """
    global DB_SESSION
    if not DB_SESSION:
        DB_SESSION = SessionLocal()
    return DB_SESSION


def close_session():
    """
    Closes a DB session if it exists
    :return: True if session was closed, otherwise False
    """
    global DB_SESSION
    try:
        if DB_SESSION:
            DB_SESSION.close()
            DB_SESSION = None
    except Exception:
        print("There is an error while closing db session!")
        return False
    return True
