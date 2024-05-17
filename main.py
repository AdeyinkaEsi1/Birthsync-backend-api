
from mongoengine import connect
from fastapi import APIRouter, FastAPI
from routes import router
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler


connect("bdsync")

app = FastAPI()

app.include_router(router)
router = APIRouter()


jobstore = MongoDBJobStore(database="bdsync", collection="jobs")
scheduler = AsyncIOScheduler(jobstores={"mongo": jobstore})
