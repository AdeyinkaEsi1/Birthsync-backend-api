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


class AccountSchema(BaseModel):
    name: str = Field(title="name", description="Full name of an account")
    email: EmailStr = Field(description="An account's email address", title="email")


class AccountResponse(AccountSchema):
    id: typing.Union[str, ObjectId]

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class AccountBasicDetail(BaseModel):
    id: typing.Union[str, ObjectId] = Field(name="id", title="id")
    name: str = Field(title="name", description="Full name of an account")
    email: EmailStr = Field(description="An account's email address", title="email")

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class AccountUpdateSchema(BaseModel):
    name: typing.Optional[str] = Field(
        default=None, title="name", description="Account's full name"
    )


class AccountPasswordChangeSchema(BaseModel):
    old_password: str
    new_password: str


class AccountRegistrationSchema(AccountSchema):
    password: str = Field(
        ...,
        title="password",
        description="An account's password",
    )


# Account Authentication

class AccountEmailAuthSchema(BaseModel):
    email: EmailStr = Field(
        ..., description="An account's email address", title="email"
    )
    password: str = Field(..., description="An account's password", title="password")


class PasswordResetSchema(BaseModel):
    token: str = Field(..., description="A valid token", title="token")
    password: str = Field(..., description="An account's password", title="password")


