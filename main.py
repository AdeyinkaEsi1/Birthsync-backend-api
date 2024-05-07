
from mongoengine import connect
from fastapi import FastAPI
from routes import router


connect("bdsync")


app = FastAPI()

app.include_router(router)

"""
{
  "username": "hamid",
  "email": "yhamid2828@gmail.com",
  "password": "hamid28"
}
"""