from typing import Any, Optional, List
from sqlalchemy import select, delete, update
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
            except Exception as e:
                print(f"Ошибка при добавлении профиля пользователя: {e}")
                await session.rollback()

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
            except Exception as e:
                print(f"Ошибка при получении задания: {e}")
                await session.rollback()

    @classmethod
    async def get_tasks(cls, task: TasksGet) -> List[OutputTasksGet]:
        async with new_session() as session:
            try:
                result = await session.execute(select(Task).where(Task.project_id == task.project_id))
                task_models = result.scalars().all()
                return [OutputTasksGet.model_validate(task_model) for task_model in task_models]
            except Exception as e:
                print(f"Ошибка при получении задания: {e}")
                await session.rollback()

    @classmethod
    async def delete_task(cls, task: TaskDelete) -> None:
        async with new_session() as session:
            try:
                result = await session.execute(select(Task).where(Task.id == task.id))
                task_to_delete = result.scalar_one_or_none()
                if task_to_delete:
                    await session.delete(task_to_delete)
                    await session.commit()
                else:
                    print(f"Задание {task.id} не найдено")
            except Exception as e:
                print(f"Ошибка при удалении задания: {e}")
                await session.rollback()

    @classmethod
    async def update_task(cls, task: TaskUpdate) -> None:
        async with new_session() as session:
            try:
                if task.title:
                    await session.execute(update(Task).where(Task.id == task.id).values(title=task.title))
                    await session.commit()
                if task.status:
                    await session.execute(update(Task).where(Task.id == task.id).values(status=task.status))
                    await session.commit()
            except Exception as e:
                print(f"Ошибка при обновлении задания: {e}")
                await session.rollback()
