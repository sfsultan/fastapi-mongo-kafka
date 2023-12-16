from typing import Annotated
import motor.motor_asyncio
import logging
from functools import cache

from rich.console import Console
from rich.logging import RichHandler
from fastapi import Header, HTTPException   
from contextlib import asynccontextmanager
from fastapi import FastAPI, Body, HTTPException, status
from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

from config import settings


console = Console(color_system="256", width=150, style="blue")


async def init_mongo(db_name: str = None, db_url: str = None, collection: str = None):
    mongo_client = motor.motor_asyncio.AsyncIOMotorClient(settings.DB_URL)
    mongo_database = mongo_client[settings.DB_NAME]
    mongo_collections = {
        "users": mongo_database.get_collection("users"),
        "dashboards": mongo_database.get_collection("dashboards"),
        "kafka": mongo_database.get_collection("kafka"),
        "widgets": mongo_database.get_collection("widgets"),
    }
    return mongo_collections



@cache
def get_logger(module_name):
    logger = logging.getLogger(module_name)
    handler = RichHandler(rich_tracebacks=True, console=console, tracebacks_show_locals=True)
    handler.setFormatter(logging.Formatter("%(name)s - [ %(threadName)s:%(funcName)s:%(lineno)d ] - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger





@asynccontextmanager
async def startup(app: FastAPI):
    app.state.logger = get_logger(__name__)
    app.state.logger.info("Starting up the application")
    app.state.mongo_collection = await init_mongo()
    yield
    app.state.logger.info("Shutting down the application...")


app = FastAPI(
    title=settings.TITLE,
    summary=settings.SUMMARY,
    lifespan=startup
)
