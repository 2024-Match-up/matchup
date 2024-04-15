from passlib.context import CryptContext
from schemas import UserInDB
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """
    비밀번호 해시값 비교
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    비밀번호 해시값 생성
    """
    return pwd_context.hash(password)

def get_user(db, username: str):
    """
    사용자 정보 데이터베이스에서 조회
    """
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(db, username: str, password: str):
    """
    사용자 인증
    """
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

