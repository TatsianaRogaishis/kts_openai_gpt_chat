"""
This module allows to operate with DB, create records, read records etc
"""

from sqlalchemy import exc

from . import models
from . import py_models

from sqlalchemy.orm import Session


def add_history(session: Session, hist: py_models.HistoryCreate) -> models.History:
    """
    Adding history record to the DB.
    :param session: DB session
    :param hist: history data (user, message)
    :return: created record with extra info (date time, id)
    """
    try:
        db_obj = models.History(user=hist.user, message=hist.message)
        session.add(db_obj)
        session.commit()
        return db_obj
    except exc.SQLAlchemyError as ex:
        print(f"There is an error while adding history line to the db: {ex}")
        raise


def get_history(session: Session, skip: int = 0, limit: int = 50) -> list[models.History]:
    """
    Getting history records from the DB.
    :param session: DB session
    :param skip: start record
    :param limit: maximum of records
    :return: list with history records
    """
    try:
        data = session.query(models.History).offset(skip).limit(limit).all()
        for h in data:
            print(f"{h.id} {h.datetime} : {h.user} : {h.message}")
        return data
    except exc.SQLAlchemyError as ex:
        print(f"There is an error while getting history from the db: {ex}")
        raise
