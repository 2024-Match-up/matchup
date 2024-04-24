from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from .routes import AuthJWT

from .schemas import UserBase
from models import User
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

def authenticate_tokens(Authorize: AuthJWT = Depends()) -> str:
    access_token = Authorize.get_jwt()
    refresh_token = Authorize.get_raw_jwt(refresh=True)

    if not access_token:
        if not refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Both access token and refresh token are missing or invalid", headers={"WWW-Authenticate": "Bearer"})
        if not Authorize.check_refresh_token():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token is invalid", headers={"WWW-Authenticate": "Bearer"})

        email = Authorize.get_jwt_subject(refresh_token)
        new_access_token = Authorize.create_access_token(subject=email)

        return new_access_token

    if not Authorize.check_jwt():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token is invalid", headers={"WWW-Authenticate": "Bearer"})

    return access_token

def create_tokens_with_headers(email: str, Authorize: AuthJWT = Depends()) -> dict:
    """
    로그인/회원가입 토큰 생성
    """
    access_token = create_access_token(email, Authorize)
    refresh_token = create_refresh_token(email, Authorize)
    return {"Authorization": f"Bearer {access_token}", "Refresh_Token": refresh_token}

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