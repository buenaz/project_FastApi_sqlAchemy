from typing import Optional, List

from sqlalchemy import select, delete, update, insert
from projects.project_models import (ProjectUpdate, ProjectAdd, ProjectGet,
                                     ProjectDelete, OutputProjectGet, AssignUser, AssignedUsers)
from db import Project, new_session, User, user_project


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

    @classmethod
    async def assign_user_for_project(cls, project: AssignUser) -> None:
        async with new_session() as session:
            try:
                result_project = await session.execute(select(Project).where(Project.id == project.id))
                project_to_assign = result_project.scalar_one_or_none()
                if not project_to_assign:
                    print(f"Проект {project.project_id} не найден.")
                    return

                result_user = await session.execute(select(User).where(User.id == project.user_id))
                user_to_assign = result_user.scalar_one_or_none()
                if not user_to_assign:
                    print(f"Пользователь {project.user_id} не найден.")
                    return

                result_assignment = await session.execute(
                    select(user_project).where(user_project.c.project_id == project.id,
                                               user_project.c.user_id == project.user_id)
                )
                existing_assignment = result_assignment.fetchone()
                if existing_assignment:
                    print(f"Пользователь {project.user_id} уже назначен на проект {project.id}.")
                    return

                await session.execute(
                    insert(user_project).values(project_id=project.id, user_id=project.user_id)
                )
                await session.commit()
            except Exception as e:
                print(f"Ошибка при назначении пользователя на проект: {e}")
                await session.rollback()

    @classmethod
    async def get_assigned_users(cls, project: AssignedUsers) -> List[AssignedUsers]:
        async with new_session() as session:
            try:
                result = await session.execute(
                    select(User.id, User.username, user_project.c.id).join(user_project,
                                                                           User.id == user_project.c.user_id)
                    .where(user_project.c.project_id == project.id)
                )
                assigned_users = result.fetchall()
                if assigned_users:
                    return [AssignedUsers.model_validate(user) for user in assigned_users]
                else:
                    print(f"Нет назначенных пользователей для проекта {project.id}.")
                    return []
            except Exception as e:
                print(f"Ошибка при получении назначенных пользователей: {e}")
                await session.rollback()
