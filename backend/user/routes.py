from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from datetime import datetime

from .crud import get_user, create_user, create_tokens_in_body, authenticate_access_token, authenticate_refresh_token, authenticate_user, update_user_profile, init_health
from .schemas import Token,UserProfileUpdate, UserBase
from logger import logger
from database import get_db
from auth import AuthJWT

router = APIRouter(
    prefix="/api/v1/user",
    tags=["user"],
)

@router.post("/token", summary="새로운 엑세스 토큰 반환", status_code=200, response_model=Token)
async def get_token(Authorize: AuthJWT = Depends()):
    """
        새로운 엑세스 토큰 반환
    """
    token = authenticate_refresh_token(Authorize=Authorize)
    return JSONResponse({"access_token": token})

@router.post("/signup", summary="회원가입", status_code=201, response_model=None)
async def signup(
                email: str = Form(..., description="User email"),
                password: str = Form(..., description="User password"),
                nickname: str = Form(..., description="User nickname"),
                birth: datetime = Form(..., description="User birth date"),
                gender: str = Form(..., description="User gender"),
                Authorize: AuthJWT = Depends(),
                db: Session = Depends(get_db),
                ):
    """
        회원가입
    """
    user = get_user(db, email)
    logger.info(user)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 가입된 아이디입니다.",
        )
    userForm = UserBase(email=email, password=password, nickname=nickname, birth=birth, gender=gender)
    
    result = create_user(db, userForm)
    
    logger.info(result)
    if result != True:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=result)
    
    health_result = init_health(db, userForm)
    logger.info(health_result)
    if health_result != True:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=health_result)
    
    response_body = create_tokens_in_body(email, Authorize)
    response_body["message"] = "유저 생성 및 로그인 성공"
    return JSONResponse(content=response_body, status_code=201)


@router.post("/login", summary="로그인", status_code=200, response_model=None)
async def login(
    email: str = Form(..., description="User email"),
    password: str = Form(..., description="User password"),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
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
    response_body = create_tokens_in_body(email, Authorize)
    logger.info(f"엑세스 토큰 기간 {Authorize._access_token_expires}")
    logger.info(f"디버깅용 유저 정보 {user.email} {user.nickname} {user.birth}")
    return JSONResponse(status_code=200, content=response_body)

@router.post("/logout", summary="로그아웃")
async def logout(
                Authorize: AuthJWT = Depends(),
                ):
    """ 
        로그아웃
    """
    access_token = Authorize.get_raw_jwt()
    email = authenticate_access_token(access_token, Authorize=Authorize)
    logger.info(f"로그아웃 유저 이메일: {email}")
    return {"message": "프런트에서 토큰 삭제하세요"}

@router.post("/profile", summary="내 정보 입력")
async def create_profile(
    nickname: str = Form(..., description="User nickname"),
    height: int = Form(..., description="키"),
    weight: int = Form(..., description="몸무게"),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    """
    사용자 프로필 생성
    """
    access_token = Authorize.get_raw_jwt()
    email = authenticate_access_token(access_token, Authorize=Authorize)
    user = get_user(db, email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found.")

    profile_data = UserProfileUpdate(nickname=nickname, height=height, weight=weight)
    result = update_user_profile(db, email, profile_data)
    if not result:
        raise HTTPException(status_code=500, detail="프로필 생성 실패")

    return JSONResponse(content={"message": "프로필 생성 완료", "email": email}, status_code=201)

@router.get("/profile", summary="내 정보 조회")
async def get_profile(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    """
    사용자 프로필 조회
    """
    access_token = Authorize.get_raw_jwt()
    email = authenticate_access_token(access_token, Authorize=Authorize)
    user = get_user(db, email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found.")

    user_profile = UserProfileUpdate(
        email=user.email,
        nickname=user.nickname,
        height=user.height,
        weight=user.weight
    )
    return JSONResponse(content=user_profile.dict(), status_code=200)

@router.put("/profile", summary="내 정보 업데이트")
async def update_profile(
    nickname: str = Form(..., description="User nickname"),
    height: int = Form(..., description="키"),
    weight: int = Form(..., description="몸무게"),
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    """
    사용자 프로필 수정
    """
    access_token = Authorize.get_raw_jwt()
    email = authenticate_access_token(access_token, Authorize=Authorize)
    profile_data = UserProfileUpdate(nickname=nickname, height=height, weight=weight)
    result = update_user_profile(db, email, profile_data)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to update profile.")

    return JSONResponse(content={"message": "Profile updated successfully", "email": email}, status_code=200)

# @router.post("/profile", summary="내 정보 입력")
# async def create_profile(
#                 height: int = Form(..., description="키"),
#                 weight: int = Form(..., description="몸무게"),
#                 waist: int = Form(..., description="허리"),
#                 leg: int = Form(..., description="다리"),
#                 pelvis: int = Form(..., description="골반"),
#                 neck: int = Form(..., description="목"),
#                 db: Session = Depends(get_db),
#                 Authorize: AuthJWT = Depends(),
#                 ):
#     """
#         사용자 프로필 생성
#     """
#     email = authenticate_access_token(Authorize=Authorize)
#     user = get_user(db, email=email)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="유저 정보가 없습니다.",
#         )
#     userForm = HealthBase(user_id=user.id, height=height, weight=weight, waist=waist, leg=leg, pelvis=pelvis, neck=neck, need=0)
#     result = create_health(db, userForm)
#     logger.info(result)
#     if result != True:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=result)
#     logger.info(f"프로필 생성 완료 {email}")
#     return JSONResponse(content={"message": "프로필 생성 완료", "email": email}, status_code=201)


# @router.get("/profile", summary="내 정보 조회")
# async def get_profile(
#                 Authorize: AuthJWT = Depends(),
#                 db: Session = Depends(get_db)
#             ):
#     """
#         사용자 프로필 조회
#     """
#     email = authenticate_access_token(Authorize=Authorize)
#     heath = get_health(db, email)
#     health_response = HealthBase(user_id=heath.user_id, height=heath.height, weight=heath.weight, waist=heath.waist, leg=heath.leg, pelvis=heath.pelvis, neck=heath.neck, need=heath.need)
#     if not heath:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="유저 프로필 정보가 없습니다.",
#         )
#     return JSONResponse(content=health_response.model_dump(), status_code=200)

# @router.put("/profile", summary="내 정보 업데이트")
# async def update_profile(
#                 height: int = Form(..., description="키"),
#                 weight: int = Form(..., description="몸무게"),
#                 waist: int = Form(..., description="허리"),
#                 leg: int = Form(..., description="다리"),
#                 pelvis: int = Form(..., description="골반"),
#                 neck: int = Form(..., description="목"),
#                 Authorize: AuthJWT = Depends(),
#                 db: Session = Depends(get_db),
#                 ):
#     """
#         사용자 프로필 수정
#     """
#     email = authenticate_access_token(Authorize=Authorize)
#     result = update_health(db, email, {"height": height, "weight": weight, "waist": waist, "leg": leg, "pelvis": pelvis, "neck": neck})
#     if not result:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="프로필 정보가 없습니다.",
#         )
#     return JSONResponse(content={"message": "프로필 수정 완료", "email": email}, status_code=200)


# @router.post("/profile", summary="내 정보 입력")
# async def create_profile(
#                 nickname: str = Form(..., description="User nickname"),
#                 height: int = Form(..., description="키"),
#                 weight: int = Form(..., description="몸무게"),
#                 db: Session = Depends(get_db),
#                 Authorize: AuthJWT = Depends(),
#                 ):
#     """
#         사용자 프로필 생성
#     """
#     email = authenticate_access_token(Authorize=Authorize)
#     user = get_user(db, email=email)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="유저 정보가 없습니다.",
#         )
#     userForm = HealthBase(user_id=user.id, nickname=nickname, height=height, weight=weight)
#     result = create_health(db, userForm)
#     logger.info(result)
#     if result != True:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=result)
#     logger.info(f"프로필 생성 완료 {email}")
#     return JSONResponse(content={"message": "프로필 생성 완료", "email": email}, status_code=201)