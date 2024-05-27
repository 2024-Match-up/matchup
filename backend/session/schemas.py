from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from models import Exercise

class SessionBase(BaseModel):
    exercise_id: int
    user_id: int
    date: datetime
    
class ReturnSession(BaseModel):
    date: datetime
    exercise: int

class SessionCreate(SessionBase):
    pass

class Session(SessionBase):
    id: int
    exercise: Exercise

    class Config:
        orm_mode = True