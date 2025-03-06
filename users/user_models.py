from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserAdd(BaseModel):
    username: str = Field(min_length=3, max_length=25)
    email: EmailStr
    role: str = Field(min_length=3, max_length=25)


class ConfigUser(UserAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserDelete(BaseModel):
    id: int


class UpdateUser(BaseModel):
    id: int
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
