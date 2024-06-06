import datetime
from pydantic import BaseModel

class SessionBase(BaseModel):
    id: int
    user_id: int
    exercise_id: int
    date: datetime.datetime
    score: int

class SessionScore(BaseModel):
    score: int
    date: datetime.datetime

    class Config:
        orm_mode = True


class FinalScoreResponse(BaseModel):
    session_id: int
    final_score: int

    class Config:
        orm_mode = True