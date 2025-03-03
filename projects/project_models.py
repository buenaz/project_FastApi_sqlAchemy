from typing import Optional
from pydantic import BaseModel, ConfigDict


class ProjectAdd(BaseModel):
    title: str
    description: str


class ProjectGet(BaseModel):
    id: int


class OutputProjectGet(BaseModel):
    id: int
    title: str
    description: str
    model_config = ConfigDict(from_attributes=True)


class ProjectDelete(BaseModel):
    id: int


class ProjectUpdate(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None


class AssignUser(BaseModel):
    user_id: int
    id: int


class AssignedUsers(BaseModel):
    user_id: int
    id: int

