from typing import Optional

from sqlalchemy import select, delete, update
from projects.project_models import (ProjectUpdate, ProjectAdd, ProjectGet,
                                     ProjectDelete, OutputProjectGet)
from db import Project, new_session


class ProjectRequests:
    @classmethod
    async def add_project(cls, project: ProjectAdd) -> int:
        async with new_session() as session:
            try:
                data = project.model_dump()
                new_project = Project(**data)
                session.add(new_project)
                await session.flush()
                await session.commit()
                return new_project.id
            except Exception as e:
                print(f"Ошибка при добавлении проекта: {e}")
                await session.rollback()

    @classmethod
    async def get_project(cls, project: ProjectGet) -> Optional[OutputProjectGet]:
        async with new_session() as session:
            try:
                result = await session.execute(select(Project).where(Project.id == project.id))
                project_to_get = result.scalar_one_or_none()
                if project_to_get:
                    return OutputProjectGet.model_validate(project_to_get)
                else:
                    print(f"Проект {project.id} не найден.")
                    return None
            except Exception as e:
                print(f"Ошибка при получении проекта: {e}")
                await session.rollback()

    @classmethod
    async def delete_project(cls, project: ProjectDelete) -> None:
        async with new_session() as session:
            try:
                result = await session.execute(select(Project).where(Project.id == project.id))
                project_to_delete = result.scalar_one_or_none()
                if project_to_delete:
                    await session.delete(project_to_delete)
                    await session.commit()
                else:
                    print(f"Проект {project.id} не найден.")
            except Exception as e:
                print(f"Ошибка при удалении проекта: {e}")
                await session.rollback()

    @classmethod
    async def update_project(cls, project: ProjectUpdate) -> None:
        async with new_session() as session:
            try:
                if project.title:
                    await session.execute(
                        update(Project).where(Project.id == project.id).values(title=project.title))
                    await session.commit()
                if project.description:
                    await session.execute(
                        update(Project).where(Project.id == project.id).values(description=project.description))
                    await session.commit()
            except Exception as e:
                print(f"Ошибка при обновлении проекта: {e}")
                await session.rollback()
