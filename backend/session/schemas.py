from pydantic import BaseModel

class SessionBase(BaseModel):
    exercise_id: int
    user_id: int

class SessionCreate(SessionBase):
    pass

class Session(SessionBase):
    id: int

    class Config:
        orm_mode = True