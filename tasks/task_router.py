from typing import Optional, List
from fastapi import APIRouter, Depends
from tasks.task_models import (TaskUpdate, TaskDelete, TaskAdd, TaskGet,
                               TasksGet, ConfigTaskAdd, OutputTasksGet)
from tasks.task_requests import TaskRequests
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/tasks",
    tags=["Таски"]
)


@router.post("/add")
async def task_add(task: TaskAdd = Depends()) -> JSONResponse:
    add_task = await TaskRequests.add_task(task)
    return JSONResponse(status_code=200, content=f"Задание {task.title} с id {add_task} добавлено к проекту {task.project_id}")


@router.get("/task_id")
async def task_get(task: TaskGet = Depends()) -> Optional[OutputTasksGet]:
    get_task = await TaskRequests.get_task(task)
    if get_task is not None:
        return get_task
    else:
        return None


@router.get("/project_id")
async def tasks_get(task: TasksGet = Depends()) -> List[OutputTasksGet]:
    get_tasks = await TaskRequests.get_tasks(task)
    if get_tasks is not None:
        return get_tasks
    else:
        return []


@router.post("/delete")
async def task_delete(task: TaskDelete = Depends()) -> JSONResponse:
    remove_task = await TaskRequests.delete_task(task)
    return JSONResponse(status_code=200, content="Задание удалено")


@router.patch("/update")
async def task_update(task: TaskUpdate = Depends()) -> JSONResponse:
    update_task = await TaskRequests.update_task(task)
    return JSONResponse(status_code=200, content=f"Данные о задании {task.id} обновлены")
