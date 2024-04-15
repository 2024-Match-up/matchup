from fastapi import APIRouter, Depends, HTTPException
from configs import jwt_algorithm, jwt_expire_minutes, jwt_secret_key


SECRET_KEY = jwt_secret_key
ALGORITHM = jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = jwt_expire_minutes


router = APIRouter(
    prefix="/api/v1/user",
    tags=["user"],
)

@router.post("/signup", summary="회원가입")
async def signup():
    """
        회원가입
    """
    return {"message": "회원가입"}

@router.post("/login", summary="로그인")
async def login():
    """
        로그인
    """
    return {"message": "로그인"}

@router.post("/logout", summary="로그아웃")
async def logout():
    """
        로그아웃
    """
    return {"message": "로그아웃"}

@router.post("/profile", summary="내 정보")
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