import traceback
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import boto3
import cv2
import numpy as np
import os
from datetime import datetime, timezone
from botocore.exceptions import NoCredentialsError 
from database import get_db
import boto3
import dotenv
from health import crud, schemas,front,side

from database import get_db, get_current_user
import logging

from health.crud import (create_health_entry_in_db,
                        submit_health_data,
                        restore_health_data,
                        download_image_from_s3)
from health.schemas import HealthBase, HealthCreate, HealthInDBBase
import models

from fastapi.security import OAuth2PasswordBearer,HTTPBearer, HTTPAuthorizationCredentials

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security = HTTPBearer()
# 의존성 함수 정의
def get_auth_header(auth: HTTPAuthorizationCredentials = Depends(security)):
    return auth.credentials

router = APIRouter(
    prefix="/api/v1/health",
    tags=["health"],
)

dotenv.load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("CREDENTIALS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("CREDENTIALS_SECRET_KEY")
AWS_REGION = os.getenv("CREDENTIALS_AWS_REGION")
S3_BUCKET_NAME = 'matchuppicture'

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

async def upload_file_to_s3(file: UploadFile, S3_BUCKET_NAME: str) -> str:
    try:
        file_name = f"{datetime.utcnow().isoformat()}-{file.filename}"
        content_type = file.content_type

        s3_client.upload_fileobj(
            file.file,
            S3_BUCKET_NAME,
            file_name,
            ExtraArgs={
                "ContentType": content_type
            }
        )

        location = s3_client.get_bucket_location(Bucket=S3_BUCKET_NAME)['LocationConstraint']
        url = f"https://{S3_BUCKET_NAME}.s3-{location}.amazonaws.com/{file_name}"
        return url
    except NoCredentialsError:
        logging.error("AWS credentials not available")
        raise HTTPException(status_code=500, detail="AWS credentials not available")
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/upload/", response_model=schemas.Health)
async def create_upload_file(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db),
    access_token: str = Depends(get_auth_header)
):  
    try:
        
        current_user = get_current_user(token = access_token, db =db)
        logging.info(f"Authenticated user: {current_user.email}")

        logging.info("Starting file upload to S3")
        image_url = await upload_file_to_s3(file, S3_BUCKET_NAME)
        logging.info(f"File uploaded to S3 at {image_url}")

        logging.info("Creating health data entry")
        health_data = schemas.HealthCreate(
            user_id=current_user.id,
            image_url=image_url,
            createdAt=datetime.utcnow()
        )

        logging.info(f"Validating health data: {health_data}")
        
        logging.info("Inserting health data into the database")
        return_data = crud.create_health_entry_in_db(db=db, health=health_data)

        created_health = return_data[0]
        is_front = return_data[1]
        
        score_dict = {}
        ##########################
        
        image = download_image_from_s3(image_url)
        
        if image is None:
            raise HTTPException(status_code=500, detail="Error occurred during image download")
        
        ## 파일 저장
        image_base_path = 'backend/images'
        
        if not os.path.exists(image_base_path):
            os.makedirs(image_base_path)
        
        ## True인 경우, front
        if is_front:
            logging.info("Processing front image")
            file_path = f"{image_base_path}/front.png"
            cv2.imwrite(file_path, image)
            score_dict = front.process_image(file_path)
        ## False인 경우, side
        else:
            logging.info("Processing side image")
            file_path = f"{image_base_path}/side.png"
            cv2.imwrite(file_path, image)
            score_dict = side.analyze_neck_angle(file_path)
            
        print(score_dict)
        ## None인 경우, 에러 발생
        if score_dict is None:
            raise HTTPException(status_code=500, detail="Error occurred during image processing")
        ## score_dict에 값이 있는 경우, 각 부위의 점수를 저장
        else:
            for key, value in score_dict.items():
                submit_health_data(db=db, user_id=current_user.id, part=key, score=value)
        ##########################
        logging.info(f"Health data inserted with ID {created_health.id}")

        
        return created_health
    except Exception as e:
        logging.error("Error occurred during file upload or DB insertion")
        logging.error(traceback.format_exc())
        return JSONResponse(status_code=500, content={"message": "Upload failed", "details": str(e)})
    
@router.get("/restore/")
def restore_health_data_route(db: Session = Depends(get_db), access_token: str = Depends(get_auth_header)):
    """
    모든 사용자의 건강 데이터를 초기화하는 함수
    """
    
    current_user = get_current_user(token = access_token, db =db)
    
    if restore_health_data(db=db, user_id=current_user.id):
        return JSONResponse(status_code=200, content={"message": "Health data restored"})
    else:
        return JSONResponse(status_code=500, content={"message": "Error occurred during health data restoration"})
    