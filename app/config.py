import os

from dotenv import load_dotenv

load_dotenv(dotenv_path="./app/.env")

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Secret key for signing cookies
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ["DEV_DATABASE_URI"]
    DEBUG = True


class LocalTestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ["TEST_LOCAL_DATABASE_URI"]
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ["PROD_DATABASE_URI"]
    POSTGRES_USER = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
    POSTGRES_DB = os.environ["POSTGRES_DB"]
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "local_testing": LocalTestingConfig,
    "production": ProductionConfig,
}
