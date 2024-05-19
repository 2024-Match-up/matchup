from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from health import schemas
import requests
from models import Health
from typing import List
import logging
import numpy as np
import cv2

def create_health_entry_in_db(db: Session, health: schemas.HealthCreate):
    user_health = db.query(Health).filter(Health.user_id == health.user_id).first()
    if user_health is None:
        raise HTTPException(status_code=400, detail="User not found")
    
    is_front = False
    if user_health.front_url == "url" and user_health.side_url == "url":
        user_health.front_url = health.image_url
        is_front = True

    elif user_health.front_url != "url" and user_health.side_url == "url":
        user_health.side_url = health.image_url
        is_front = False
        
    else:
        raise HTTPException(status_code=400, detail="Both URLs are already set")

    db.add(user_health)
    db.commit()
    db.refresh(user_health)
    return [user_health, is_front]

def get_health_entries(db: Session, user_id: int) -> List[schemas.HealthInDB]:
    return db.query(Health).filter(Health.user_id == user_id).order_by(Health.createdAt).all()
    
def submit_health_data(db: Session, user_id: int, part:str, score:int) -> bool:
    """
    각 부위의 점수를 저장하는 함수
    """
    try:
        db_health = db.query(Health).filter(Health.user_id == user_id).first()
        
        if db_health is None:
            raise HTTPException(status_code=400, detail="User not found")
        
        logging.info(f"Updating health data for part: {part} with score: {score}")
        
        if part == "pelvis":
            db_health.pelvis = score
        elif part == "waist":
            db_health.waist = score
        elif part == "leg":
            db_health.leg = score
        elif part == "neck":
            db_health.neck = score
        else:
            raise HTTPException(status_code=400, detail="Part not found")
        db.add(db_health)
        db.commit()
        db.refresh(db_health)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
def restore_health_data(db: Session,user_id: int):
    """
    모든 사용자의 건강 데이터를 초기화하는 함수
    """
    try:
        logging.info("Restoring health data")
        db_health = db.query(Health).filter(Health.user_id == user_id).first()
        if db_health is None:
            raise HTTPException(status_code=400, detail="User not found")
        db_health.front_url = "url"
        db_health.side_url = "url"
        db_health.pelvis = 0
        db_health.waist = 0
        db_health.leg = 0
        db_health.neck = 0
        db.add(db_health)
        db.commit()
        db.refresh(db_health)
        return True
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
def download_image_from_s3(image_url: str):
    """
    S3에서 이미지를 다운로드하는 함수
    """
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        return image
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error downloading image: {e}")
    return user_health

def get_user_images(db: Session, user_id: int):
    return db.query(Health).filter(Health.user_id == user_id).first()


