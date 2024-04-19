from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import *
from schemas import *
from typing import Annotated, List, Union
from mongoengine import NotUniqueError, DoesNotExist
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Controllers:
    
    def root(token: Annotated[str, Depends(oauth2_scheme)]):
        return {"token": token}
        # return {"message": "ROOT ENDPOINT"}

    SECRET_KEY = "aa78aca0d83af707dcac482ce4226d14ae75d80a4ba8656705f7543ea00e55f4"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def list_birthdays() -> List[PersonResponseSchema]:
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
        


        
