import os
DB_HOST = os.environ['POSTGRES_HOST']
DB_NAME = os.environ['POSTGRES_DB']
DB_USER = os.environ['POSTGRES_USER']
DB_PASS = os.environ['POSTGRES_PASSWORD']


class DevelopmentConfig:
    TESTING = False
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = "sqlite:///development.db"
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"


class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test_database.db"
