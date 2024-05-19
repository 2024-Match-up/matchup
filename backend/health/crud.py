# from sqlalchemy.orm import Session
# from health import schemas
# from models import Health,User
# from datetime import datetime

# def create_health_entry_in_db(db: Session, health: schemas.HealthCreate ):

#     users_health = db.get(Health).get(health.user_id)
#     front = users_health.front_url
#     side = users_health.side_url
#     if(front == "url" and side == "url"):
#         save_health = Health(
#             user_id = health.uesr_id,
#             front_url = health.image_url,
#             createdAt=datetime.utfnow()
#         )
#     elif(front != "url" and side == "url"):
#         save_health = Health(
#             user_id = health.uesr_id,
#             side_url = health.image_url,
#             createdAt=datetime.utfnow()
#         )

#     db.add(save_health)
#     db.commit()
#     db.refresh(save_health)
#     return save_health

from sqlalchemy.orm import Session
from datetime import datetime, timezone
from health import schemas
from models import Health

def create_health_entry_in_db(db: Session, health: schemas.HealthCreate):
    user_health = db.query(Health).filter(Health.user_id == health.user_id).first()
    
    if user_health.front_url == "url" and user_health.side_url == "url":
        save_health = Health(
            user_id=health.user_id,
            front_url=health.image_url,
            createdAt=datetime.now(timezone.utc)
        )
    elif user_health.front_url != "url" and user_health.side_url == "url":
        save_health = Health(
            user_id=health.user_id,
            side_url=health.image_url,
            createdAt=datetime.now(timezone.utc)
        )
    else:
        raise HTTPException(status_code=400, detail="Both URLs are already set")

    db.add(save_health)
    db.commit()
    db.refresh(save_health)
    return save_health