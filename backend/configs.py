from dotenv import load_dotenv
import os

load_dotenv()

sql_alchemy_database_url = os.environ.get('SQLALCHEMY_DATABASE_URL')
jwt_secret_key = os.environ.get('JWT_SECRET_KEY')
jwt_algorithm = os.environ.get('JWT_ALGORITHM')
jwt_expire_minutes = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRE_MINUTES'))
jwt_refresh_days = int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRE_MINUTES'))
