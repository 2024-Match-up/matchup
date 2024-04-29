from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi_another_jwt_auth import AuthJWT

from .crud import get_user, create_user, create_tokens_in_body, authenticate_access_token, authenticate_refresh_token, authenticate_user
from .schemas import Token, UserBase, Settings
from logger import logger
from database import get_db

router = APIRouter(
    prefix="/api/v1/user",
    tags=["user"],
)

@AuthJWT.load_config
def get_config():
    return Settings()

@router.post("/token", summary="새로운 엑세스 토큰 반환", status_code=200, response_model=Token)
async def get_token(Authorize: AuthJWT = Depends()):
    """
        새로운 엑세스 토큰 반환
    """
    token = authenticate_refresh_token(Authorize)
    return JSONResponse({"access_token": token})

@router.post("/signup", summary="회원가입", status_code=201, response_model=None)
async def signup(
                email: str = Form(..., description="User email"),
                password: str = Form(..., description="User password"),
                nickname: str = Form(..., description="User nickname"),
                birth: datetime = Form(..., description="User birth date"),
                gender: str = Form(..., description="User gender"),
                db: Session = Depends(get_db),
                Authorize: AuthJWT = Depends()
                ):
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
    response_body = create_tokens_in_body(email, Authorize)
    response_body["message"] = "유저 생성 및 로그인 성공"
    return JSONResponse(content=response_body, status_code=201)

@router.post("/login", summary="로그인", status_code=200, response_model=None)
async def login(
    email: str = Form(..., description="User email"),
    password: str = Form(..., description="User password"),
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
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
    response_headers = create_tokens_in_body(email, Authorize)
    logger.info(f"엑세스 토큰 기간 {Authorize._access_token_expires}")
    return JSONResponse(status_code=200, content=response_headers)

@router.post("/logout", summary="로그아웃")
async def logout(
    Authorize: AuthJWT = Depends(),
):
    """
        로그아웃
    """
    email = authenticate_access_token(Authorize=Authorize)
    return {"message": "프런트에서 토큰 삭제하세요"}

@router.post("/profile", summary="내 정보 입력")
async def create_profile(
    Authorize: AuthJWT = Depends()
):
    """
        사용자 프로필 생성
    """
    email = authenticate_access_token(Authorize=Authorize)
    return {"message": "프로필 생성 완료", "email": email}

@router.get("/profile", summary="내 정보 조회")
async def get_profile(
    Authorize: AuthJWT = Depends(),
):
    """
        사용자 프로필 조회
    """
    # return {"access_token": access_token, "profile": get_user(Authorize.get_jwt_subject())}

@router.put("/profile", summary="내 정보 업데이트")
async def update_profile(
    Authorize: AuthJWT = Depends(),
):
    """
        사용자 프로필 수정
    """
    # return {"access_token": access_token, "profile": get_user(Authorize.get_jwt_subject())}
