from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi_another_jwt_auth.exceptions import AuthJWTException

import os
import models
from database import engine, SessionLocal
from user import routes as user_routes
from exercise import routes as exercise_routes
from logger import logger
import sys
import dotenv
import boto3

from user import routes as user_routes
from exercise import routes as exercise_routes
from health import routes as health_routes
from session import routes as session_routes
from models import Exercise
from exercise.mediapipe.exercise.waist import WaistExercise
from exercise.mediapipe.exercise.squat import SquatExercise
from exercise.mediapipe.exercise.leg import LegExercise
from exercise.mediapipe.exercise.neck import NeckExercise

dotenv.load_dotenv()

app = FastAPI()
router = APIRouter(prefix="/api/v1")
app.include_router(health_routes.router)
app.include_router(user_routes.router)
app.include_router(exercise_routes.router)
app.include_router(session_routes.router)

client_s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("CREDENTIALS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("CREDENTIALS_SECRET_KEY"),
    region_name=os.getenv("CREDENTIALS_AWS_REGION")
)

# origins = [
#     "http://127.0.0.1:5173",  # 또는 "http://localhost:5173"
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def insert_initial_data():
    db = SessionLocal()
    try:
        exercises = [
            Exercise(
                name="neck",
                count=5,
                set=3,
                time=0,
                coordinate_list=[NeckExercise.get_neck_coordinates()],
            ),
            Exercise(
                name="hip",
                count=5,
                set=3,
                time=0,
                coordinate_list=[SquatExercise.get_squat_coordinates()],
            ),
            Exercise(
                name="leg",
                count=5,
                set=3,
                time=10,
                coordinate_list=[LegExercise.get_lunge_coordinates()]
            ),
            Exercise(
                name="waist",
                count=5,
                set=3,
                time=0,
                coordinate_list=WaistExercise.get_waist_coordinates(),
            )
        ]
        db.add_all(exercises)
        db.commit()
    finally:
        db.close()

try:
    models.Base.metadata.create_all(bind=engine)
    logger.info("테이블 생성 완료")
    insert_initial_data()  # 테이블 생성 후 초기 데이터 삽입
    logger.info("초기 데이터 삽입 완료")
except Exception as e:
    logger.error("테이블 생성 실패")
    logger.info(e)
    sys.exit(1)

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"메시지": exc.message}
    )

@app.get("/")
def hello():
    return {"message": "메인페이지입니다"}

@app.get("/test-s3")
async def test_s3_connection():
    try:
        response = client_s3.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        return {"buckets": buckets}
    except Exception as e:
        logger.error(f"Failed to connect to S3: {e}")
        raise HTTPException(status_code=500, detail="Failed to connect to S3")
