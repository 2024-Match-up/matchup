from dotenv import load_dotenv
import os

load_dotenv()

sql_alchemy_database_url = os.environ.get('SQLALCHEMY_DATABASE_URL')
JWT_SECRET_KET = os.environ.get('JWT_SECRET_KEY')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')
JWT_ACCESS_EXPIRE_MINUTES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRE_MINUTES'))
JWT_REFRESH_EXPIRE_DAYS = int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRE_DAYS'))
CREDENTIALS_ACCESS_KEY = os.environ.get('CREDENTIALS_ACCESS_KEY')
CREDENTIALS_SECRET_KEY = os.environ.get('CREDENTIALS_SECRET_KEY')
CREDENTIALS_AWS_REGION = os.environ.get('CREDENTIALS_AWS_REGION')