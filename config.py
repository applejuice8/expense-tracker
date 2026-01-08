import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # General
    FLASK_APP = 'wsgi.py'
    FLASK_DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
