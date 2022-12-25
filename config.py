class DevelopmentConfig:
    TESTING = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///development.db"


class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test_database.db"
