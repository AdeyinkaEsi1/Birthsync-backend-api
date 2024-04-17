from pydantic import BaseModel, Field
from datetime import date


class PersonBaseSchema(BaseModel):
    name: str = ...
    birth_date: date = Field(..., description="Date of birth")
    extra_info: str = None
    

class PersonResponseSchema(PersonBaseSchema):
    pass