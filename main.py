
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response


from bson import ObjectId
from pymongo import ReturnDocument
from api.models import *
from api.routers import users, dashboard, kafka, widgets

from api.dependencies import get_logger, init_mongo, app


app.include_router(users.router)
app.include_router(dashboard.router)
app.include_router(kafka.router)
app.include_router(widgets.router)


