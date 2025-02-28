from fastapi import APIRouter, Depends
from models import UserAdd, GetUserId, UserDelete, UpdateUserEmail
from requests import UserRequests
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/users",
    tags=["Юзеры"]
)


@router.post("/add")
async def add_user(user: UserAdd = Depends()) -> GetUserId:
    new_user = await UserRequests.add_user(user)
    return {"id": new_user}


@router.get("")
async def get_users() -> list[UserAdd]:
    users = await UserRequests.get_users()
    return users


@router.post("/delete")
async def delete_user(user: UserDelete = Depends()) -> JSONResponse:
    remove_user = await UserRequests.delete_user(user)
    return JSONResponse(status_code=200, content="Пользователь удален")


@router.post("/update_email")
async def update_user_email(user: UpdateUserEmail = Depends()) -> JSONResponse:
    update_email = await UserRequests.update_user_email(user)
    return JSONResponse(status_code=200, content="email обновлен")
