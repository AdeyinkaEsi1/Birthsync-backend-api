from fastapi import BackgroundTasks, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from models import *
from schemas import *
from typing import List
from mongoengine import NotUniqueError, DoesNotExist
from passlib.context import CryptContext
from settings import *
from logging import getLogger
from emai_task import send_email_reminder
from scheduler import scheduler, jobstore
from main import *
import datetime
from datetime import timedelta
from uuid import uuid4
from utils.auth import auth_account, verify_password, jwt_encode


logger = getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="")


class Controllers:
    
    @classmethod
    def sign_up(cls, payload: AccountRegSchema):
        try:
            hashed_password = pwd_context.hash(payload.hashed_password)
            data = BaseAccount(
                username=payload.username,
                hashed_password=hashed_password,
                email=payload.email
            )
            data.save()
            return {"message": "User created successfully"}
        except NotUniqueError:
            raise HTTPException(
                status_code=406,
                detail="Data not unique"
            )


    @classmethod
    def sign_in(cls, bg_tasks: BackgroundTasks, payload: Signin_Schema):
        try:
            user = BaseAccount.objects.get(username=payload.username)
        except:
            raise HTTPException(
                status_code=404,
                detail="Details not found"
            )
        if user and verify_password(payload.password, user.hashed_password):
            try:
                access_token = jwt_encode(data={"sub": user.username})
            except:
                raise HTTPException(
                status_code=404,
                detail="jwt encoding error."
            )
        response = JSONResponse(
            {
                "user": {
                    "id": str(user.id),
                    "username": payload.username,
                    "email": payload.email,
                }
            }
        )
        response.set_cookie(
            key="token",
            value=access_token,
            secure=True,
            samesite="none",
            expires=(
                datetime.datetime.utcnow()
                + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            ).strftime("%a, %d %b %Y %H:%M:%S GMT"),
        )
        return response
    

    @classmethod
    def list_birthdays(cls, user: BaseAccount = Depends(auth_account))-> List[PersonResponseSchema]:
        data = Person.objects.all()
        bday_data = []
        for bd in data:
            bday_data.append(
                {"name": bd.name,
                 "birth_date": bd.birth_date,
                 "extra_info": bd.extra_info,
                 "id": str(bd.id)}
            )
        scheduler.print_jobs()
        return bday_data
    
    
    @classmethod
    def list_users(cls)-> List[AccountResponseSchema]:
        return BaseAccount.objects.all()
    

    @classmethod
    def add_birthday(cls, data: PersonCreateSchema, background_tasks: BackgroundTasks):
        success = {"message": "Data created successfully"}
        try:
            new_data = Person(name=data.name, birth_date=data.birth_date, extra_info=data.extra_info)
            new_data.save()
            Controllers.schedule_birthday_reminder()
            return success
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error encountered --> {e}"
            )    

    
    @classmethod
    def update_birthday(cls, data_id: str, data: PersonUpdateSchema):
        try:
            update_data = data.model_dump(exclude_unset=True)
            Person.objects(id=data_id).update(**update_data)
            return {"message": "Data successfully updated"}
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Data not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    
    @classmethod
    def get_birthday(cls, data_id: str) -> PersonResponseSchema:
        try:
            person = Person.objects.get(id=data_id)
            person_data = {
            "name": person.name,
            "birth_date": person.birth_date,
            "extra_info": person.extra_info,
            "id": str(person.id)
            }
        except Exception:
            raise HTTPException(status_code=404, detail="Data not found")
        return person_data
    
    
    @classmethod
    def delete_birthday(cls, data_id: str):
        try:
            data = Person.objects.get(id=data_id)
            data.delete()
        except Exception:
            raise HTTPException(status_code=404, detail="Data not found")
        return {"message": "Data deleted successfully"}     
        

    def send_reminder(name):
        print(f"Today is {name}'s birthday")
        # send_email_reminder("adeyinkah.28@gmail.com", name)
        

    @classmethod
    def schedule_birthday_reminder(cls):
        today = datetime.date.today()
        two_days_time = today + timedelta(days=2)
        for person in Person.objects():
            user_bdate = person.birth_date
        date_model = DateModel(provided_birthday=user_bdate)
        prov_birthday = date_model.provided_birthday
        if two_days_time - prov_birthday <= timedelta(days=2):
           provided_birthday = prov_birthday
        reminder_time = datetime.datetime.combine(provided_birthday, datetime.datetime.min.time()) + timedelta(hours=6, minutes=42)
        job_id = f'job_{str(uuid4())}'
        scheduler.add_job(Controllers.send_reminder, 'date', run_date=reminder_time, args=[person.name], id=job_id, jobstore="mongo")
        scheduler.print_jobs()
        scheduler.start()

    