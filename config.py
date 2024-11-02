import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres:postgres@db:5432/postgres'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SCHEDULER_HOURS = int(os.environ.get('SCHEDULER_HOURS', 24))
