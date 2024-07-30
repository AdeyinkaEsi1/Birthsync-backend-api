from mongoengine import connect
from fastapi import APIRouter, FastAPI
import pymongo
from routes import router
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import settings
from database import connect_db

""" Apscheduler DB"""
# connect("bdsync")
connect_db()


app = FastAPI()

app.include_router(router)

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# 18870884
