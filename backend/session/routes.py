from fastapi import APIRouter, Depends, HTTPException
from session import schemas, crud
from sqlalchemy.orm import Session
from database import get_db
import logging
from database import get_current_user
from health.routes import get_auth_header
from auth import AuthJWT


router = APIRouter(
    prefix="/api/v1/session",
    tags=["session"],
)

@router.get("/", summary="세션 정보 조회", response_model=List[schemas.Session])
def read_sessions(
    Authorize: AuthJWT = Depends(), 
    db: Session = Depends(get_db)
):
    Authorize.jwt_required()
    current_user_email = Authorize.get_jwt_subject()
    user = crud.get_user_by_email(db, email=current_user_email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_sessions_by_user_id(db, user_id=user.id)