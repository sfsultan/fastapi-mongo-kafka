import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Represents the configuration settings for the application. All of the these variables
    should be set in the OS enviornment. If a variable is not found there a default is used from here.

    TITLE = Title of the App
    SUMMARY = Summary of the App
    ENVIRONMENT = local, production
    DB_URL = URL of the MongoDB server
    DB_NAME = Name of the database
    ACCESS_TOKEN_EXPIRE_MINUTES = JWT Access token expiry
    REFRESH_TOKEN_EXPIRE_MINUTES = JWT Refresh token expiry
    ALGORITHM = Which algorith to use for the JWT encryption
    JWT_SECRET_KEY = JWT Access token secret key used for the encryption
    JWT_REFRESH_SECRET_KEY = JWT Refresh token secret key used for the encryption
    KAFKA_SERVERS = Comma separated list of Kafka brokers e.g. localhost:9092
    KAFKA_TOPIC_PARTITIONS = Number of partitions to set for topics that are being created
    KAFKA_REPLICATION_FACTOR = Message replication factor for the new topics
    KAFKA_CONSUMER_TIMEOUT = Amount of time in (ms) for the Kafka client to wait before polling the topics for new messages
    KAFKA_CONSUMER_MAX_RECORDS = Number of max records that can be fetched at a time from the topics
    """


    TITLE: str = os.getenv("TITLE", "FastAPI + MongoDB + Kafka Project")
    SUMMARY: str = os.getenv("SUMMARY", "Application uses FastAPI and RABC to add a ReST API to MongoDB + Kafka implementation.")
    
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "local")

    DB_URL: str = os.getenv("MONGODB_URL", "mongodb://farmer:tractor@192.168.1.12:27017/?retryWrites=true&w=majority")
    DB_NAME: str = os.getenv("MONGO_DB", "main_db")
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 * 100
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', "main_secret")
    JWT_REFRESH_SECRET_KEY: str = os.getenv('JWT_REFRESH_SECRET_KEY', "refresh_secret")

    KAFKA_SERVERS: str = os.getenv("KAFKA_SERVERS", "192.168.1.12:9092")
    KAFKA_TOPIC_PARTITIONS: int = os.getenv("KAFKA_TOPIC_PARTITIONS", 1)
    KAFKA_REPLICATION_FACTOR: int = os.getenv("KAFKA_REPLICATION_FACTOR", 1)
    KAFKA_CONSUMER_TIMEOUT: int = os.getenv("KAFKA_CONSUMER_TIMEOUT", 5000)
    KAFKA_CONSUMER_MAX_RECORDS: int = os.getenv("KAFKA_CONSUMER_MAX_RECORDS", 200)

settings = Settings()