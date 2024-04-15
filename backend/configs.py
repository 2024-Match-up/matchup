from dotenv import load_dotenv
import os

load_dotenv()

sql_alchemy_database_url = os.environ.get('SQLALCHEMY_DATABASE_URL')
