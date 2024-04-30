from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from .routes import AuthJWT

from .schemas import UserBase, HealthBase
from models import User, Health
from logger import logger
from datetime import timedelta
from configs import JWT_ACCESS_EXPIRE_MINUTES

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

def authenticate_refresh_token(Authorize: AuthJWT = Depends()) -> str:
    """
    리프레시 토큰 인증 및 엑세스 토큰 반환
    """
    Authorize.jwt_refresh_token_required()
    email = Authorize.get_jwt_subject()
    logger.info(f"유저 이메일: {email} 리프레시 토큰 확인 완료")
    return create_access_token(email, Authorize)

def create_tokens_in_body(email: str, Authorize: AuthJWT = Depends()) -> dict:
    """
    로그인/회원가입 토큰 생성
    """
    access_token = create_access_token(email, Authorize)
    refresh_token = create_refresh_token(email, Authorize)
    return {"access_token" : access_token, "refresh_token" : refresh_token}

def create_access_token(email: str, Authorize: AuthJWT = Depends()):
    """
    엑세스 토큰 생성
    """
    Authorize._access_token_expires = timedelta(minutes=JWT_ACCESS_EXPIRE_MINUTES)
    return Authorize.create_access_token(subject=email)

def create_refresh_token(email: str, Authorize: AuthJWT = Depends()):
    """
    리프레시 토큰 생성
    """
    return Authorize.create_refresh_token(subject=email)

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

def create_health(db, health: HealthBase):
    """
    프로필 생성
    """
    try:
        user_health = Health(**health.model_dump())
        db.add(user_health)
        db.commit()
        db.refresh(user_health)
    except Exception as e:
        db.rollback()
        return e
    return True

def get_health(db, email: str):
    """
    프로필 조회
    """
    health_data = db.query(Health).join(User).filter(User.email == email).first()
    if health_data:
        return health_data
    else:
        return False

def update_health(db, email: str, health: dict):
    """
    프로필 수정
    """
    health_data = db.query(Health).join(User).filter(User.email == email).first()
    if not health_data:
        return False
    health_dict = health_data.__dict__
    logger.info(health_dict)
    for k, v in health.items():
        if health_dict[k] != v:
            logger.info(f"프로필 수정: key: {k}, value: {health_dict[k]} -> {v}")
            setattr(health_data, k, v)
    db.commit()
    return True
