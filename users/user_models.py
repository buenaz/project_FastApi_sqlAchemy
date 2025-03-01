from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserAdd(BaseModel):
    username: str
    email: str


class ConfigUser(UserAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserDelete(BaseModel):
    id: int


class UpdateUserEmail(BaseModel):
    id: int
    email: str