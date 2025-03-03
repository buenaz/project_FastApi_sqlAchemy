from typing import Optional
from pydantic import BaseModel, ConfigDict


class TaskAdd(BaseModel):
    title: str
    status: str
    project_id: int


class ConfigTaskAdd(TaskAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TaskGet(BaseModel):
    id: int


class TasksGet(BaseModel):
    project_id: int


class OutputTasksGet(BaseModel):
    id: int
    title: str
    status: str
    project_id: int
    model_config = ConfigDict(from_attributes=True)


class TaskDelete(BaseModel):
    id: int


class TaskUpdate(BaseModel):
    id: int
    title: Optional[str] = None
    status: Optional[str] = None
