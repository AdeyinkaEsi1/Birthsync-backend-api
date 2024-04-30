from typing import Optional, Union
from pydantic import BaseModel, Field, EmailStr
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
    name: Optional[str] = None
    birth_date: Optional[date] = None
    extra_info: Optional[str] = None

    class Config:
        orm_mode = True

        # =======================

class AccountDetailsSchema(BaseModel):
    username: str
    email: EmailStr


class AccountRegSchema(AccountDetailsSchema):
    hashed_password: str

class Signin_Schema(AccountDetailsSchema):
    password: Union[str, int]


class AccountResponseSchema(AccountDetailsSchema):
    pass

class AccountUpdateSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    class Config:
        orm_mode = True

