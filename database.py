from mongoengine import connect
from dotenv import load_dotenv, find_dotenv
import os


dotenv_path = find_dotenv()

if not dotenv_path:
    raise Exception("Could not find .env file")
load_dotenv(dotenv_path, override=True)

MONGO_URI = os.getenv("MONGO_URI")
# print(MONGO_URI)
if not MONGO_URI:
    raise Exception("MONGO_URI is not set in the environment variables")
def connect_db():
    try:
        connect(host=MONGO_URI)
        print("Connected successfully")
    except Exception as e:
        print("The following error occurred:", e)
        raise
    
connect_db()