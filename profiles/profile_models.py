from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ProfileAdd(BaseModel):
    bio: str = Field(min_length=10, max_length=100)
    phone: str = Field(pattern=r"^\+?\d{1,3}?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$")
    skill: str = Field(min_length=3, max_length=20)
    social_link: str
    user_id: int


class OutputProfileGet(ProfileAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ProfileDelete(BaseModel):
    user_id: int


class ProfileGet(BaseModel):
    user_id: int


class ProfileUpdate(BaseModel):
    user_id: int
    bio: Optional[str] = None
    phone: Optional[str] = None
    skill: Optional[str] = None
    social_link: Optional[str] = None
