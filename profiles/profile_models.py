from typing import Optional
from pydantic import BaseModel, ConfigDict


class ProfileAdd(BaseModel):
    bio: str
    phone: str
    skill: str
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
