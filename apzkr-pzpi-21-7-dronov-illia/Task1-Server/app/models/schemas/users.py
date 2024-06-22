from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, field_validator

from app.models.db.user import UserRoles
from app.utilities.validators.payload.datetime import validate_date_format
from app.utilities.validators.payload.user import (
    validate_name,
    validate_passport_number,
    validate_password,
)


class UserBase(BaseModel):
    first_name: str
    last_name: str
    birth_date: str
    gender: Literal["male", "female"]
    email: EmailStr
    passport_number: str

    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, value):
        return validate_name(value, "first_name")

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, value):
        return validate_name(value, "last_name")

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, value):
        return validate_date_format(value, "birth_date")

    @field_validator("passport_number")
    @classmethod
    def validate_passport_number(cls, value):
        return validate_passport_number(value)


class UserRegister(UserBase):
    role: UserRoles
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        return validate_password(value)


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[str] = None
    gender: Optional[Literal["male", "female"]] = None
    email: Optional[EmailStr] = None
    passport_number: Optional[str] = None


class UserData(UserBase):
    id: int
    role: str


class UserLoginInput(BaseModel):
    email: EmailStr
    password: str


class UserLoginOutput(BaseModel):
    token: str


class NewPasswordInput(BaseModel):
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate(cls, value: str):
        return validate_password(value)


class PasswordChangeInput(NewPasswordInput):
    old_password: str


class PasswordChangeOutput(BaseModel):
    message: str
