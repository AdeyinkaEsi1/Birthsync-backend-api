from typing import Union, Optional
from pydantic import BaseModel, Field
from datetime import date



class PersonBaseSchema(BaseModel):
    name: str = ...
    birth_date: date = Field(..., description="Date of birth")
    extra_info: str


class PersonResponseSchema(PersonBaseSchema):
    id: str


class PersonCreateSchema(PersonBaseSchema):
    pass


class PersonUpdateSchema(BaseModel):
    name: Optional[str]
    birth_date: Optional[date]
    extra_info: Optional[str]

    class Config:
        orm_mode = True
