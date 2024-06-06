# from sqlalchemy.orm import Session
# import models
# from models import Session
# from datetime import datetime
# from models import Session as SessionModel

# def create_session(db:Session, user_id: int, exercise_id: int, date: datetime):
#     new_session = Session(user_id=user_id, exercise_id=exercise_id, date=date)
#     db.add(new_session)
#     db.commit()
#     db.refresh(new_session)
#     return new_session


# def get_sessions_by_user_id(db:Session, user_id: int):
#     return db.query(SessionModel).filter(SessionModel.user_id == user_id).all()


# def get_latest_session_by_user_and_exercise(db, user_id: int, exercise_id: int):
#     session = db.query(SessionModel).filter(SessionModel.user_id == user_id, SessionModel.exercise_id == exercise_id).order_by(models.Session.date.desc()).first()
#     return session

from sqlalchemy.orm import Session
from datetime import datetime
import models
from models import Session as SessionModel  # 데이터베이스 모델의 Session 클래스 임포트

def create_session(db: Session, user_id: int, exercise_id: int, date: datetime):
    new_session = SessionModel(user_id=user_id, exercise_id=exercise_id, date=date)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

def get_sessions_by_user_id(db: Session, user_id: int):
    return db.query(SessionModel).filter(SessionModel.user_id == user_id).all()

def get_latest_session_by_user_and_exercise(db: Session, user_id: int, exercise_id: int):
    session = db.query(SessionModel).filter(SessionModel.user_id == user_id, SessionModel.exercise_id == exercise_id).order_by(SessionModel.date.desc()).first()
    return session
