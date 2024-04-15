from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from .crud import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_user, create_user
from .schemas import Token, UserBase
from database import get_db

router = APIRouter(
    prefix="/api/v1/user",
    tags=["user"],
)

@router.post("/signup", summary="회원가입", response_model=Token)
async def signup(
    email: str = Form(..., description="User email"),
    password: str = Form(..., description="User password"),
    nickname: str = Form(..., description="User nickname"),
    birth: datetime = Form(..., description="User birth date"),
    gender: str = Form(..., description="User gender"),
    db: Session = Depends(get_db)
) -> Token:
    """
        회원가입
    """
    user = get_user(db, email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 가입된 아이디입니다.",
        )
    userForm = UserBase(email=email, password=password, nickname=nickname, birth=birth, gender=gender)
    result = create_user(db, userForm)
    if result != True:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=result)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.post("/login", summary="로그인", response_model=Token)
async def login(
    email: str = Form(..., description="User email"),
    password: str = Form(..., description="User password"),
    db: Session = Depends(get_db)
) -> Token:
    """
        로그인
    """
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="비밀번호나 아이디가 틀렸습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.post("/logout", summary="로그아웃")
async def logout():
    """
        로그아웃
    """
    return {"message": "프런트에서 토큰 삭제하세요"}

@router.post("/profile", summary="내 정보 입력")
async def profile():
    """
        사용자 프로필 입력
    """
    return {"message": "내 정보 입력"}

@router.get("/profile", summary="내 정보 조회")
async def profile():
    """
        사용자 프로필 조회
    """
    return {"message": "내 정보 조회"}

@router.put("/profile", summary="내 정보 업데이트")
async def profile():
    """
        사용자 프로필 업데이트
    """
    return {"message": "내 정보 업데이트"}