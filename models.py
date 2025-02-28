from pydantic import BaseModel, ConfigDict


class UserAdd(BaseModel):
    username: str
    email: str


class UserDelete(BaseModel):
    id: int


class ConfigUser(UserAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class GetUserId(BaseModel):
    id: int


class UpdateUserEmail(BaseModel):
    id: int
    email: str
