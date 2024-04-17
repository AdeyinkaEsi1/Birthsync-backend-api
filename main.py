from mongoengine import connect

connect("bdsync")

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