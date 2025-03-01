from typing import Optional
from fastapi import APIRouter, Depends
from profiles.profile_models import ProfileAdd, ProfileGet, ProfileDelete, ProfileUpdate, OutputProfileGet
from profiles.profile_requests import ProfileRequests
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/profiles",
    tags=["Профили"]
)


@router.post("/add")
async def profile_add(profile: ProfileAdd = Depends()) -> JSONResponse:
    add_profile = await ProfileRequests.add_profile(profile)
    return JSONResponse(status_code=200, content=f"Профиль {profile.id} добавлен")


@router.get("/")
async def profile_get(profile: ProfileGet = Depends()) -> Optional[OutputProfileGet]:
    get_profile = await ProfileRequests.get_profile(profile)
    if get_profile is not None:
        return OutputProfileGet.model_validate(get_profile)
    else:
        return None


@router.post("/delete")
async def profile_delete(profile: ProfileDelete = Depends()) -> JSONResponse:
    remove_profile = await ProfileRequests.delete_profile(profile)
    return JSONResponse(status_code=200, content="Профиль пользователя удален")


@router.patch("/update")
async def profile_update(profile: ProfileUpdate = Depends()) -> JSONResponse:
    update_profile = await ProfileRequests.update_profile(profile)
    return JSONResponse(status_code=200, content="Профиль пользователя обновлен")
