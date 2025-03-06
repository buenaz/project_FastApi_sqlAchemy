from typing import Optional, List
from fastapi import APIRouter, Depends
from projects.project_models import (ProjectUpdate, ProjectAdd, ProjectGet,
                                     ProjectDelete, OutputProjectGet, AssignUser, AssignedUsers, OutputAssignedUsers)
from projects.project_requests import ProjectRequests
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/projects",
    tags=["Проекты"]
)


@router.post("/add")
async def project_add(project: ProjectAdd = Depends()) -> JSONResponse:
    add_project = await ProjectRequests.add_project(project)
    return JSONResponse(status_code=200, content=f"Проект {project.title} добавлен. Id проекта {add_project}")


@router.get("/")
async def project_get(project: ProjectGet = Depends()) -> Optional[OutputProjectGet]:
    get_project = await ProjectRequests.get_project(project)
    if get_project is not None:
        return OutputProjectGet.model_validate(get_project)
    else:
        return None


@router.post("/delete")
async def project_delete(project: ProjectDelete = Depends()) -> JSONResponse:
    remove_project = await ProjectRequests.delete_project(project)
    return JSONResponse(status_code=200, content="Проект удален")


@router.patch("/update")
async def project_update(project: ProjectUpdate = Depends()) -> JSONResponse:
    update_project = await ProjectRequests.update_project(project)
    return JSONResponse(status_code=200, content=f"Данные о проекте {project.id} обновлены")


@router.post("/add_user")
async def assign_user(project: AssignUser = Depends()) -> JSONResponse:
    add_user = await ProjectRequests.assign_user_for_project(project)
    return JSONResponse(status_code=200, content=f"Пользователь с ID {project.user_id} добавлен к проекту {project.id}")


@router.get("/get_users")
async def get_assigned_users(project: AssignedUsers = Depends()) -> List[OutputAssignedUsers]:
    assigned_users = await ProjectRequests.get_assigned_users(project)
    return assigned_users

