from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from health import schemas
from models import Health

def create_health_entry_in_db(db: Session, health: schemas.HealthCreate):
    user_health = db.query(Health).filter(Health.user_id == health.user_id).first()
    if user_health is None:
        raise HTTPException(status_code=400, detail="User not found")
    
    if user_health.front_url == "url" and user_health.side_url == "url":
        user_health.front_url = health.image_url

    elif user_health.front_url != "url" and user_health.side_url == "url":
        user_health.side_url = health.image_url
    else:
        raise HTTPException(status_code=400, detail="Both URLs are already set")

    db.add(user_health)
    db.commit()
    db.refresh(user_health)
    return user_health

def get_user_images(db: Session, user_id: int):
    return db.query(Health).filter(Health.user_id == user_id).first()