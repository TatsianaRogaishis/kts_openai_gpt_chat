import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text

from .database import Base


class History(Base):
    """
    A model for working with history item for db.
    """
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String)
    datetime = Column(DateTime, default=datetime.datetime.now(), nullable=False)
    message = Column(Text, )
