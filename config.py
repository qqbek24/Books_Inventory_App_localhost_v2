import os
from dotenv import load_dotenv
from pathlib import Path

base_dir = Path(__file__).resolve().parent
env_file = base_dir / '.env'
load_dotenv(env_file)


class Config:
    SECRET_KEY = os.environ.get('APP_SECRET_KEY')
    GOOGLE_BOOKS_API_KEY = os.environ.get('GOOGLE_BOOKS_API_KEY')
    DEBUG_MODE = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # DB_USER_LOGIN = os.environ.get('DB_USER_LOGIN')
    # DB_USER_PASS = os.environ.get('DB_USER_PASS')
    # S_HOST = os.environ.get('S_HOST')
    # S_DB = os.environ.get('S_DB')
