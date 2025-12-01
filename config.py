import os
from pathlib import Path

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cricket-analytics-secret-key-change-in-production'
    BASE_DIR = Path(__file__).parent
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE_DIR / 'data' / 'cricket_data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
