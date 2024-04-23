from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from configs import jwt_algorithm, jwt_expire_minutes, jwt_secret_key, jwt_refresh_days
from .schemas import TokenData, UserBase
from models import User
from logger import logger


SECRET_KEY = jwt_secret_key
ALGORITHM = jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = jwt_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = jwt_refresh_days

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
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

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    JWT 엑세스 토큰 생성
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    """
    JWT 리프레시 토큰 생성
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire, "refresh": "True"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def is_access_token_valid(token: str) -> bool:
    """
    엑세스 토큰 확인
    """
    try:
        decoded_access_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if 'access_token' in decoded_access_token:
            expiration_time = datetime.fromtimestamp(decoded_access_token['exp'])
            return expiration_time > datetime.now(timezone.utc)
        else:
            return False
    except jwt.ExpiredSignatureError:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="엑세스 토큰이 만료 되었습니다",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.InvalidTokenError:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="엑세스 토큰이 유효하지 않습니다",
                headers={"WWW-Authenticate": "Bearer"},
            )
def is_refresh_token_valid(token: str) -> bool:
    """
    리프레시 토큰 확인
    """
    try:
        decoded_refresh_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if "refresh_token" in decoded_refresh_token:
            expiration_time = datetime.fromtimestamp(decoded_refresh_token['exp'])
            return expiration_time > datetime.now(timezone.utc)
        else:
            return False
    except jwt.ExpiredSignatureError:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="리프레시 토큰이 만료 되었습니다",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.InvalidTokenError:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="리프레시 토큰이 유효하지 않습니다",
                headers={"WWW-Authenticate": "Bearer"},
            )

def return_email_from_token(token: str) -> str:
    try:
        decoded_access_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if 'email' in decoded_access_token:
            email = decoded_access_token['email']
            return email
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="엑세스 토큰이 유효하지 되었습니다. 이메일이 확인 되지 않음",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="엑세스 토큰이 만료 되었습니다",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.InvalidTokenError:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="엑세스 토큰이 유효하지 않습니다",
                headers={"WWW-Authenticate": "Bearer"},
            )

async def create_user(db, user: UserBase):
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
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        return e
    return True

async def create_profile(db, user: UserBase):
    pass