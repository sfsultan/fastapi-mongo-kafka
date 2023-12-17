import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Represents the configuration settings for the application.

    """
    TITLE: str = "FastAPI + MongoDB + Kafka Project"
    SUMMARY: str = "Application uses FastAPI and RABC to add a ReST API to MongoDB + Kafka implementation."
    
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "local")
    TESTING: str = os.getenv("TESTING", "0")
    UP: str = os.getenv("UP", "up")
    DOWN: str = os.getenv("DOWN", "down")
    WEB_SERVER: str = os.getenv("WEB_SERVER", "web_server")

    DB_URL: str = os.getenv("MONGODB_URL", "mongodb://farmer:tractor@192.168.1.12:27017/?retryWrites=true&w=majority")
    DB_NAME: str = os.getenv("MONGO_DB", "main_db")
    TEST_DB_NAME: str = os.getenv("MONGO_TEST_DB", "")
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', "main_secret")   # should be kept secret
    JWT_REFRESH_SECRET_KEY: str = os.getenv('JWT_REFRESH_SECRET_KEY', "refresh_secret")    # should be kept secret

    KAFKA_SERVERS: str = os.getenv("KAFKA_SERVERS", "192.168.1.12:9093")

settings = Settings()