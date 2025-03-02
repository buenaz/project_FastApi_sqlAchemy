from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserAdd(BaseModel):
    username: str
    email: str
    role: str


class ConfigUser(UserAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserDelete(BaseModel):
    id: int


class UpdateUser(BaseModel):
    id: int
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
