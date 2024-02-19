from datetime import datetime
from typing import Optional
from uuid import UUID

from email_validator import validate_email
from pydantic import BaseModel, EmailStr, validator


class UserBase(BaseModel):
    first_name: str
    second_name: str
    email: EmailStr

    class Config:
        from_attributes = True

    @validator('email')
    def validate_email(value: EmailStr) -> EmailStr:
        email_info = validate_email(value, check_deliverability=True)
        email = email_info.normalized
        return email


class UserCreate(UserBase):
    uid: UUID
    hashed_password: str


class UserPreCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    uid: UUID
    registered_at: datetime


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    second_name: Optional[str] = None
