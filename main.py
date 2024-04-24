
from mongoengine import connect
from fastapi import FastAPI
from routes import router


connect("bdsync")

SECRET_KEY = ""
ALGORITHM = ""
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

app.include_router(router)

"""
{
  "username": "hamid",
  "email": "hamid@example.com",
  "password": "hamid28"
}
"""