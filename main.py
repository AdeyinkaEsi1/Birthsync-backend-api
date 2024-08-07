from mongoengine import connect
from fastapi import FastAPI
import uvicorn
from routes import router
from fastapi.middleware.cors import CORSMiddleware
import os
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    