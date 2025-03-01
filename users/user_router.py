from fastapi import APIRouter, Depends
from users.user_requests import UserRequests
from users.user_models import UserAdd, UserDelete, UpdateUser
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/users",
    tags=["Юзеры"]
)


@router.post("/add")
async def add_user(user: UserAdd = Depends()) -> JSONResponse:
    new_user = await UserRequests.add_user(user)
    return JSONResponse(status_code=200, content=f"Пользовать {user.username} c Id {new_user} добавлен")


@router.get("")
async def get_users() -> list[UserAdd]:
    users = await UserRequests.get_users()
    return users


@router.post("/delete")
async def delete_user(user: UserDelete = Depends()) -> JSONResponse:
    remove_user = await UserRequests.delete_user(user)
    return JSONResponse(status_code=200, content="Пользователь удален")


@router.patch("/update")
async def update_user_email(user: UpdateUser = Depends()) -> JSONResponse:
    update_email = await UserRequests.update_user_email(user)
    return JSONResponse(status_code=200, content=f"Пользователь {user.id} обновлен")
