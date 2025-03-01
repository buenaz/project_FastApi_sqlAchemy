from typing import Optional
from pydantic import BaseModel, ConfigDict


class ProfileAdd(BaseModel):
    bio: str
    phone: str
    user_id: int


class OutputProfileGet(BaseModel):
    bio: str
    phone: str
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class ProfileDelete(BaseModel):
    user_id: int


class ProfileGet(BaseModel):
    user_id: int


class ProfileUpdate(BaseModel):
    user_id: int
    bio: Optional[str] = None
    phone: Optional[str] = None
