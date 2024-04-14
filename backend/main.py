from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import models
from database import SessionLocal, engine

app = FastAPI()

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
    print("테이블 생성 완료")
except:
    print("이미 테이블이 생성되어 있습니다.")



@app.get("/hello")
def hello():
    return {"message": "안녕하세요 파이보"}
