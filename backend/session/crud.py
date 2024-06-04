from sqlalchemy.orm import Session
import models
from models import Session
from datetime import datetime

def create_session(db: Session, user_id: int, exercise_id: int, date: datetime):
    new_session = Session(user_id=user_id, exercise_id=exercise_id, date=date)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session


def get_sessions_by_user_id(db: Session, user_id: int):
    return db.query(models.Session).filter(models.Session.user_id == user_id).all()


def get_latest_session_by_user_and_exercise(db: Session, user_id: int, exercise_id: int):
    return db.query(models.Session).filter(models.Session.user_id == user_id, models.Session.exercise_id == exercise_id).order_by(models.Session.date.desc()).first()