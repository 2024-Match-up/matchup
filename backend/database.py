# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, Session
# import configs

# from passlib.context import CryptContext
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt
# from sqlalchemy.orm import Session

# import dotenv
# import os

# dotenv.load_dotenv()
# JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
# JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

# # mysql 이랑 연결
# SQLALCHEMY_DATABASE_URL = configs.sql_alchemy_database_url

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# def get_db() -> Session:
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# def get_current_user(token: str, db: Session = Depends(get_db)):
#     from user import crud
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = crud.get_user(db, email=email)
#     if user is None:
#         raise credentials_exception
#     return user


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import configs

from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

import dotenv
import os

dotenv.load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

# MySQL과 연결
SQLALCHEMY_DATABASE_URL = configs.sql_alchemy_database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str, db: Session = Depends(get_db)):
    from user import crud
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, email=email)
    if user is None:
        raise credentials_exception
    return user

def insert_initial_data():
    from models import Exercise
    from backend.exercise.mediapipe.exercise.waist import get_waist_coordinates  # 필요한 함수 임포트
    db = SessionLocal()
    try:
        exercises = [
            Exercise(
                name="neck",
                count=3,
                set=3,
                time=0,
                coordinate_list=[],
            ),
            Exercise(
                name="waist",
                count=10,
                set=3,
                time=0,
                coordinate_list=get_waist_coordinates(),
            ),
            Exercise(
                name="hip",
                count=10,
                set=3,
                time=0,
                coordinate_list=[],
            ),
            Exercise(
                name="leg",
                count=1,
                set=3,
                time=10,
                coordinate_list=[]
            )
        ]
        db.add_all(exercises)
        db.commit()
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    insert_initial_data()

if __name__ == "__main__":
    init_db()
