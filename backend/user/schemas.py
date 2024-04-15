from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserBase(BaseModel):
    email: str
    nickname: str
    password: str
    birth: str
    gender: str

class UserCreate(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password: str

