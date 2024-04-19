from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import *
from schemas import *
from typing import Annotated, List, Union
from mongoengine import NotUniqueError, DoesNotExist
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
import datetime


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Controllers:
    
    # def root(token: Annotated[str, Depends(oauth2_scheme)]):
    #     return {"token": token}
        # return {"message": "ROOT ENDPOINT"}

    SECRET_KEY = "SECRET_KEY"
    ALGORITHM = ""
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    """
    response.set_cookie(
                key="token",
                value=token,
                secure=True,
                samesite="none",
                expires=(
                    datetime.datetime.utcnow()
                    + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
                ).strftime("%a, %d %b %Y %H:%M:%S GMT"),
            )
            ret
    """


    def jwt_encode(payload: dict):
        """Encode JWT using account's payload"""
        return jwt.encode(
            {
                **payload,
                "exp": datetime.datetime.now(datetime.UTC)
                + datetime.timedelta(minutes=Controllers.ACCESS_TOKEN_EXPIRE_MINUTES),
            },
          Controllers.SECRET_KEY,
            algorithm="HS256",
        )


    def jwt_decode(token: str):
        """Decode JWT using account's payload"""
        return jwt.decode(token, Controllers.SECRET_KEY, algorithms=["HS256"])


    def auth_account(
    request: Request = Annotated[Request, Depends(oauth2_scheme)]
    ):
        """Get current account from JWT token. If token is invalid, raise an exception.
        If token is valid, return account object.
        """
        token = request.cookies.get("token")
        if token is None:
            raise HTTPException(
                headers={"WWW-Authenticate": "Bearer"},
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        
        try:
            payload = Controllers.jwt_decode(token)
        except Exception:
            # logger.exception("auth_account(jwt_decode): Detokenization failed")
            raise HTTPException(
                headers={"WWW-Authenticate": "Bearer"},
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        try:
            account = Person.objects.get(({"id": payload["id"]}))
        except DoesNotExist:
            raise HTTPException(
                headers={"WWW-Authenticate": "Bearer"},
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return account


    def list_birthdays(auth = Depends(auth_account)) -> List[PersonResponseSchema]:
        if auth.account:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Authenticated account has no team"
            )
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
    
    
    def add_birthday(data: PersonCreateSchema):
        try:
            new_data = Person(name=data.name, birth_date=data.birth_date, extra_info=data.extra_info)
            new_data.save()
            return {"message": "Data created successfully"}
        except NotUniqueError:
            raise HTTPException(status_code=406, detail="Data not unique")
        
    
    def update_birthday(data_id: str, data: PersonUpdateSchema):
        try:
            update_data = data.model_dump(exclude_unset=True)
            Person.objects(id=data_id).update(**update_data)
            return {"message": "Data successfully updated"}
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Data not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    
    def get_birthday(data_id: str) -> PersonResponseSchema:
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
    
    
    def delete_birthday(data_id: str):
        try:
            data = Person.objects.get(id=data_id)
            data.delete()
        except Exception:
            raise HTTPException(status_code=404, detail="Data not found")
        return {"message": "Data deleted successfully"}     
        


        
