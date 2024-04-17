from models import Person
from schemas import PersonResponseSchema
from typing import List

class Controllers:
    
    def root():
        return {"message": "ROOT ENDPOINT"}
    

    def list_birthdays() -> List[PersonResponseSchema]:
        data = Person.objects.all()
        bday_data = []
        for bd in data:
            bday_data.append(
                {"name": bd.name,
                 "birthday": bd.birth_date,
                 "extra_info": bd.extra_info}
            )
        return bday_data