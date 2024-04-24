from dotenv import load_dotenv
import os

load_dotenv()

sql_alchemy_database_url = os.environ.get('SQLALCHEMY_DATABASE_URL')
JWT_SECRET_KET = os.environ.get('JWT_SECRET_KEY')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')
JWT_ACCESS_EXPIRE_MINUTES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRE_MINUTES'))
JWT_REFESH_EXPIRE_DAYS = int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRE_DAYS'))
