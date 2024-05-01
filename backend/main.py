from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi_another_jwt_auth.exceptions import AuthJWTException

import models
from database import engine
from user import routes as user_routes
from exercise import routes as exercise_routes
from logger import logger
import sys

app = FastAPI()
router = APIRouter(prefix="/api/v1")
app.include_router(user_routes.router)
app.include_router(exercise_routes.router)

origins = [
    "http://127.0.0.1:5173",    # 또는 "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    models.Base.metadata.create_all(bind=engine)
    logger.info("테이블 생성 완료")
except Exception as e:
    logger.error("테이블 생성 실패")
    logger.info(e)
    # sys.exit(1)

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"메시지": exc.message}
    )

@app.get("/")
def hello():
    return {"message": "메인페이지입니다"}
