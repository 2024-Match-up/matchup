from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi_another_jwt_auth import AuthJWT

from .schemas import UserProfileUpdate, UserBase
from models import User, Health
from logger import logger
from datetime import timedelta
from configs import JWT_ACCESS_EXPIRE_MINUTES
import random
import string

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """
    비밀번호 해시값 비교
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    비밀번호 해시값 생성
    """
    return pwd_context.hash(password)

def get_user(db, email: str):
    """
    사용자 정보 데이터베이스에서 조회
    """
    user_dict = db.query(User).filter(User.email == email).first()
    if user_dict:
        return user_dict
    else:
        False

def authenticate_user(db, email: str, password: str):
    """
    사용자 인증
    """
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def authenticate_access_token(Authorize: AuthJWT) -> str:
    """
    엑세스 토큰 인증 및 유저 이메일 반환
    """
    Authorize.jwt_required()
    email = Authorize.get_jwt_subject()
    logger.info(f"유저 이메일: {email} 엑세스 토큰 확인 완료")
    return email

def authenticate_refresh_token(Authorize: AuthJWT) -> str:
    """
    리프레시 토큰 인증 및 엑세스 토큰 반환
    """
    Authorize.jwt_refresh_token_required()
    email = Authorize.get_jwt_subject()
    logger.info(f"유저 이메일: {email} 리프레시 토큰 확인 완료")
    return create_access_token(email, Authorize)

def create_tokens_in_body(email: str, Authorize: AuthJWT) -> dict:
    """
    로그인/회원가입 토큰 생성
    """
    access_token = create_access_token(email, Authorize)
    refresh_token = create_refresh_token(email, Authorize)
    return {"access_token" : access_token, "refresh_token" : refresh_token}

def create_access_token(email: str, Authorize: AuthJWT):
    """
    엑세스 토큰 생성
    """
    Authorize._access_token_expires = timedelta(minutes=JWT_ACCESS_EXPIRE_MINUTES)
    return Authorize.create_access_token(subject=email)

def create_refresh_token(email: str, Authorize: AuthJWT):
    """
    리프레시 토큰 생성
    """
    return Authorize.create_refresh_token(subject=email)

def init_health(db, user: UserBase):
    """
    초기 health 테이블 데이터 초기화
    """
    try:
        db_user = db.query(User).filter(User.email == user.email).first()
        db_health = Health(
            user_id = db_user.id,
        )
        if db_user:
            db.add(db_health)
            db.commit()
            db.refresh(db_health)
    except Exception as e:
        db.rollback()
        return e
    return True
    
def create_user(db, user: UserBase):
    """
    사용자 생성
    """
    check_user = get_user(db, user.email)
    if check_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 가입된 아이디입니다.",
        )
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    try:
        db_user = User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        return e
    return True

def update_user_profile(db, email: str, profile_data: UserProfileUpdate) -> bool:
    user = get_user(db, email)
    if not user:
        return False
    try:
        user.nickname = profile_data.nickname
        user.height = profile_data.height
        user.weight = profile_data.weight
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(e)
        return False