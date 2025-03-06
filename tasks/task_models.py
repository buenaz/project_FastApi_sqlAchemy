from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class TaskAdd(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    status: str = Field(min_length=3, max_length=25)
    project_id: int


class ConfigTaskAdd(TaskAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TaskGet(BaseModel):
    id: int


class TasksGet(BaseModel):
    project_id: int


class OutputTasksGet(TaskAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TaskDelete(BaseModel):
    id: int


class TaskUpdate(BaseModel):
    id: int
    title: Optional[str] = None
    status: Optional[str] = None
