from mongoengine import connect
from fastapi import FastAPI
from routes import router


connect("bdsync")

app = FastAPI()

app.include_router(router)


"""
--- Person model(doc)

--- Personbaseschema(bmodle)
--- Personcreateschema(perdonbase)
--- Personresponseschema(personbase)
--- Personupdateschema(personbase)

endpoints
-get == List Bdays
-get == get bday
-post == add bday
-put == upd bday
-del == del bday
"""