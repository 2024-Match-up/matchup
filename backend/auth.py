from pydantic import BaseModel
from datetime import timedelta
from fastapi_another_jwt_auth import AuthJWT
from configs import JWT_ALGORITHM, JWT_SECRET_KET, JWT_ACCESS_EXPIRE_MINUTES, JWT_REFRESH_EXPIRE_DAYS

class Settings(BaseModel):
    authjwt_secret_key: str = JWT_SECRET_KET
    access_expires: int = timedelta(minutes=JWT_ACCESS_EXPIRE_MINUTES)
    refresh_expires: int = timedelta(days=JWT_REFRESH_EXPIRE_DAYS)
    authjwt_token_location: set = {"headers"}
    authjwt_header_name: str = "Authorization"
    authjwt_header_type: str = "Bearer"
    authjwt_algorithm: str = JWT_ALGORITHM
    authjwt_decode_algorithms: list = [JWT_ALGORITHM]

@AuthJWT.load_config
def get_config():
    return Settings()