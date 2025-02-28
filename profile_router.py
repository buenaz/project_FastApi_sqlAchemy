from fastapi import APIRouter, Depends
from models import ProfileAdd, ProfileGet, ProfileDelete, ConfigProfile, UpdatePhone, UpdateBio, GetProfileId
from requests import ProfileRequests
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/profile",
    tags=["Профили"]
)


@router.post("/add")
async def add_user(profile: ProfileAdd = Depends()) -> GetProfileId:
    return {"id": await ProfileRequests.add_profile(profile)}


@router.get("/")
async def get_users(profile: ProfileGet = Depends()) -> ProfileAdd:
    return await ProfileRequests.get_profile(profile)


@router.post("/delete")
async def delete_user(profile: ProfileDelete = Depends()) -> JSONResponse:
    remove_profile = await ProfileRequests.delete_profile(profile)
    return JSONResponse(status_code=200, content="Профиль пользователя удален")