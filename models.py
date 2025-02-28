from pydantic import BaseModel, ConfigDict


class UserAdd(BaseModel):
    username: str
    email: str


class ConfigUser(UserAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserDelete(BaseModel):
    id: int


class GetUserId(BaseModel):
    id: int


class UpdateUserEmail(BaseModel):
    id: int
    email: str


class ProfileAdd(BaseModel):
    bio: str
    phone: str
    user_id: str


class ConfigProfile(ProfileAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ProfileDelete(BaseModel):
    user_id: int


class ProfileGet(BaseModel):
    user_id: int


class UpdateBio(BaseModel):
    user_id: int
    bio: str


class UpdatePhone(BaseModel):
    user_id: int
    phone: str


class GetProfileId(BaseModel):
    id: int
