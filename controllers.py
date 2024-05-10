
from fastapi import BackgroundTasks, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import *
from schemas import *
from typing import Annotated, List, Union
from mongoengine import NotUniqueError, DoesNotExist
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
import datetime
import settings
from logging import getLogger
from apscheduler.schedulers.background import BackgroundScheduler
from task import send_email_reminder



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
        if user and Controllers.verify_password(payload.password, user.hashed_password):
            try:
                access_token = Controllers.jwt_encode(data={"sub": user.username})
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
                + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            ).strftime("%a, %d %b %Y %H:%M:%S GMT"),
        )
        return response

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return pwd_context.verify(
            plain_password,
            hashed_password
        )
        

    @classmethod
    def jwt_encode(cls, data: dict):
        return jwt.encode(
            {
                **data,
                "exp": datetime.datetime.utcnow()
                + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            },
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )


    @classmethod
    def jwt_decode(cls, token: str):
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Could not decode token"
            )
        
        

    async def auth_account(request: Request = Annotated[Request, Depends(oauth2_scheme)]):
        """Handles authentication"""
        token = request.cookies.get("token")
        if token is None:
            raise HTTPException(
                headers={"WWW-Authenticate": "Bearer"},
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        try:
            payload  = Controllers.jwt_decode(token)
        except Exception:
            logger.exception("auth_account(jwt_decode): Detokenization failed")
            raise HTTPException(
                headers={"WWW-Authenticate": "Bearer"},
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials(token expired)",
            )
        try:
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(
                headers={"WWW-Authenticate": "Bearer"},
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="(username None)Invalid authentication credentials",
            )
        except JWTError:
            raise HTTPException(
                headers={"WWW-Authenticate": "Bearer"},
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="(JWT ERROR)Invalid authentication credentials",
            )
    

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
        return bday_data
    
    
    @classmethod
    def list_users(cls)-> List[AccountResponseSchema]:
        user = BaseAccount.objects.all()
        users = []
        for _ in user:
            users.append(
                {
                    "username": _.username,
                    "email": _.email
                }
            )
        return users
    

    
    @classmethod
    async def add_birthday(cls, data: PersonCreateSchema, background_tasks: BackgroundTasks):
        success = {"message": "Data created successfully"}
        try:
            new_data = Person(name=data.name, birth_date=data.birth_date, extra_info=data.extra_info)
            new_data.save()
            try:
                sched = BackgroundScheduler()
                def reminder():
                    send_email_reminder("adeyinkah.28@gmail.com", data.name)
                reminder_time = datetime.datetime.combine(data.birth_date, datetime.datetime.min.time()) + timedelta(hours=23, minutes=15)
                sched.add_job(reminder, 'date', run_date=reminder_time)
                try:
                    sched.start()
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Scheduler failed: {e}")
            except Exception as e:
                raise HTTPException(status_code=500, detail="scheduler operation failed")
            return success
        except NotUniqueError:
            raise HTTPException(status_code=406, detail="Data not unique")
        
    
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
        

