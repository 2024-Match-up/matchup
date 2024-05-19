from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class HealthBase(BaseModel):
    waist: int
    leg: int
    pelvis: int
    neck: int
    side_url : str
    front_url : str
    need: int

class HealthCreate(BaseModel):
    user_id : int
    image_url : str
    createdAt: datetime

class HealthInDBBase(HealthBase):
    id: int
    user_id: int
    createdAt: datetime

    class Config:
        orm_mode = True

class Health(HealthInDBBase):
    pass

class HealthInDB(HealthInDBBase):
    pass

class HealthLimited(BaseModel):
    waist: int
    leg: int
    pelvis: int
    neck: int
    user_id: int
    createdAt: datetime

    class Config:
        orm_mode = True

class HealthURLs(BaseModel):
    user_id : int
    front_url: str
    side_url: str

