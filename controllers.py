from fastapi import HTTPException
from models import *
from schemas import *
from typing import List
from mongoengine import NotUniqueError

class Controllers:
    
    def root():
        return {"message": "ROOT ENDPOINT"}
    

    def list_birthdays() -> List[PersonResponseSchema]:
        data = Person.objects.all()
        bday_data = []
        for bd in data:
            bday_data.append(
                {"name": bd.name,
                 "birth_date": bd.birth_date,
                 "extra_info": bd.extra_info}
            )
        return bday_data
    
    def add_birthday(data: PersonCreateSchema):
        try:
            new_data = Person(name=data.name, birth_date=data.birth_date, extra_info=data.extra_info)
            new_data.save()
            return {"message": "Data created successfully"}
        except NotUniqueError:
            raise HTTPException(status_code=406, detail="data not unique")
        
