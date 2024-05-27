from mongoengine import connect
from fastapi import APIRouter, FastAPI, HTTPException
from routes import router
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware


connect("bdsync")

app = FastAPI()

app.include_router(router)
router = APIRouter()


jobstore = MongoDBJobStore(database="bdsync", collection="jobs")
scheduler = AsyncIOScheduler(jobstores={"mongo": jobstore})


# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
