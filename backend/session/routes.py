from fastapi import APIRouter, Depends, HTTPException
from session import schemas, crud
from sqlalchemy.orm import Session
from database import get_db
import logging
from database import get_current_user
from health.routes import get_auth_header
from auth import AuthJWT
from crud import get_sessions_by_user_id
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from typing import List

security = HTTPBearer()

def get_auth_header(auth: HTTPAuthorizationCredentials = Depends(security)):
    return auth.credentials


router = APIRouter(
    prefix="/api/v1/session",
    tags=["session"],
)
"""
유저별 특정날에 어떤 운동을 했는지 조회
"""
@router.get("/", summary="세션 정보 조회", response_model=List[schemas.ReturnSession])
def read_sessions(
    accessToken:str =Depends(get_auth_header), 
    db: Session = Depends(get_db)
):
    user = get_current_user(db = db, token = accessToken)
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    sessions = get_sessions_by_user_id(db = db, user_id = user.id)
    
    session_list = []
    
    for session in sessions:
        session_list.append({
            "date": session.date,
            "exercise": session.exercise_id,
        })
    
    
    return session_list