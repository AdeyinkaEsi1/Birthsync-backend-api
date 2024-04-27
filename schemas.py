from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import date
import typing
from bson import ObjectId


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
"""
create acctdet schema
acct reg schema
sign in schema
acct response schema
acct update schema
"""

class AccountDetailsSchema(BaseModel):
    username: str
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str
    

class AccountRegSchema(AccountDetailsSchema):
    hashed_password: str

class Sign_inSchema(AccountDetailsSchema):
    password: str

class AccountResponseSchema(AccountDetailsSchema):
    pass

class AccountUpdateSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    class Config:
        orm_mode = True

