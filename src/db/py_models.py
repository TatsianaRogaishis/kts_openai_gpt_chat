from datetime import datetime
from pydantic import BaseModel


class ItemBase(BaseModel):
    """
    Base model for history item.
    """
    user: str
    message: str


class HistoryCreate(ItemBase):
    """
    A model for creating history line.
    """

    class Config:
        from_attributes = True


class HistoryItem(ItemBase):
    """
    A model for getting history item with full description.
    """
    id: int
    datetime: datetime

    class Config:
        from_attributes = True
