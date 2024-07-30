# scheduler.py
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.background import BackgroundScheduler

jobstore = MongoDBJobStore(database="bdsync", collection="jobs")
scheduler = BackgroundScheduler(jobstores={"mongo": jobstore})
