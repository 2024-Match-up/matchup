from pydantic import BaseModel
from datetime import datetime, timedelta
from configs import JWT_ALGORITHM, JWT_SECRET_KET, JWT_ACCESS_EXPIRE_MINUTES, JWT_REFRESH_EXPIRE_DAYS

class Token(BaseModel):
    access_token: str
    refresh_token: str

class Settings(BaseModel):
    authjwt_secret_key: str = JWT_SECRET_KET
    access_expires: int = timedelta(minutes=JWT_ACCESS_EXPIRE_MINUTES)
    refresh_expires: int = timedelta(days=JWT_REFRESH_EXPIRE_DAYS)
    authjwt_token_location: set = {"headers"}
    authjwt_header_name: str = "Authorization"
    authjwt_header_type: str = "Bearer"
    authjwt_algorithm: str = JWT_ALGORITHM
    authjwt_decode_algorithms: list = [JWT_ALGORITHM]

class UserBase(BaseModel):
    email: str
    nickname: str
    password: str
    birth: datetime
    gender: str

class HealthBase(BaseModel):
    user_id: int
    waist: int
    leg: int
    pelvis: int
    neck: int
    need: int
    
class UserProfileUpdate(BaseModel):
    nickname: str
    height: int
    weight: int


