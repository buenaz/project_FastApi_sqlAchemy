from typing import Any, Optional, List

from fastapi import HTTPException, status
from sqlalchemy import select, delete, update
from sqlalchemy.exc import SQLAlchemyError

from tasks.task_models import TaskAdd, TaskGet, TasksGet, TaskDelete, TaskUpdate, ConfigTaskAdd, OutputTasksGet
from db import User, Profile, Project, Task, new_session


class TaskRequests:
    @classmethod
    async def add_task(cls, task: TaskAdd) -> int:
        async with new_session() as session:
            try:
                data = task.model_dump()
                new_task = Task(**data)
                session.add(new_task)
                await session.flush()
                await session.commit()
                return new_task.id
            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Ошибка базы данных при добавлении задания: {e}")
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Неожиданная ошибка при добавлении задания: {e}")

    @classmethod
    async def get_task(cls, task: TaskGet) -> Optional[OutputTasksGet]:
        async with new_session() as session:
            try:
                result = await session.execute(select(Task).where(Task.id == task.id))
                task_to_get = result.scalar_one_or_none()
                if task_to_get:
                    return OutputTasksGet.model_validate(task_to_get)
                else:
                    print(f"Задание {task.id} не найдено.")
                    return None
            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Ошибка базы данных при получении задания: {e}")
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Неожиданная ошибка при получении задания: {e}")

    @classmethod
    async def get_tasks(cls, task: TasksGet) -> List[OutputTasksGet]:
        async with new_session() as session:
            try:
                result = await session.execute(select(Task).where(Task.project_id == task.project_id))
                task_models = result.scalars().all()
                return [OutputTasksGet.model_validate(task_model) for task_model in task_models]
            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Ошибка базы данных при получения заданий: {e}")
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Неожиданная ошибка при получения заданий: {e}")

    @classmethod
    async def delete_task(cls, task: TaskDelete) -> bool:
        async with new_session() as session:
            try:
                result = await session.execute(select(Task).where(Task.id == task.id))
                task_to_delete = result.scalar_one_or_none()
                if task_to_delete:
                    await session.delete(task_to_delete)
                    await session.commit()
                    return True
                else:
                    print(f"Задание {task.id} не найдено")
                    return False
            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Ошибка базы данных при удалении задания: {e}")
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Неожиданная ошибка при удалении задания: {e}")

    @classmethod
    async def update_task(cls, task: TaskUpdate) -> bool:
        async with new_session() as session:
            try:
                task_to_update = await session.execute(select(Task).where(Task.id == task.id))
                task_to_update = task_to_update.scalar_one_or_none()

                if not task_to_update:
                    print(f"Задание с id {task.id} не найден.")
                    return False

                update_values = {}

                if task.title:
                    update_values["title"] = task.title
                if task.status:
                    update_values["status"] = task.status

                if update_values:
                    await session.execute(update(Task).where(Task.id == task.id).values(update_values))
                    await session.commit()
                    return True
                else:
                    return True
            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Ошибка базы данных при обновлении задания: {e}")
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Неожиданная ошибка при обновлении задания: {e}")
