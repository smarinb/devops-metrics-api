from pydantic import BaseModel, EmailStr
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    viewer = "viewer"


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.viewer


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
