from typing import Optional, List

from fastapi import HTTPException, status
from sqlalchemy import select, delete, update, insert
from sqlalchemy.exc import SQLAlchemyError

from projects.project_models import (ProjectUpdate, ProjectAdd, ProjectGet,
                                     ProjectDelete, OutputProjectGet, AssignUser, AssignedUsers, OutputAssignedUsers)
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
            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Ошибка базы данных при добавлении проекта: {e}")
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Неожиданная ошибка при добавлении проекта: {e}")

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
            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Ошибка базы данных при получении проекта: {e}")
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Неожиданная ошибка при получении проекта: {e}")

    @classmethod
    async def delete_project(cls, project: ProjectDelete) -> bool:
        async with new_session() as session:
            try:
                result = await session.execute(select(Project).where(Project.id == project.id))
                project_to_delete = result.scalar_one_or_none()
                if project_to_delete:
                    await session.delete(project_to_delete)
                    await session.commit()
                    return True
                else:
                    print(f"Проект {project.id} не найден.")
                    return False
            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Ошибка базы данных при удалении проекта: {e}")
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Неожиданная ошибка при удалении проекта: {e}")

    @classmethod
    async def update_project(cls, project: ProjectUpdate) -> bool:
        async with new_session() as session:
            try:
                project_to_update = await session.execute(select(Project).where(Project.id == project.id))
                project_to_update = project_to_update.scalar_one_or_none()

                if not project_to_update:
                    print(f"Проект с ID {project.id} не найден")
                    return False

                update_values = {}

                if project.title:
                    update_values["title"] = project.title
                if project.description:
                    update_values["description"] = project.description

                if update_values:
                    await session.execute(update(Project).where(Project.id == project.id).values(update_values))
                    await session.commit()
                    return True
                else:
                    return True
            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Ошибка базы данных при удалении проекта: {e}")
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Неожиданная ошибка при удалении проекта: {e}")

    @classmethod
    async def assign_user_for_project(cls, project: AssignUser) -> bool:
        async with new_session() as session:
            try:
                result_project = await session.execute(select(Project).where(Project.id == project.id))
                project_to_assign = result_project.scalar_one_or_none()
                if not project_to_assign:
                    print(f"Проект {project.project_id} не найден.")
                    return False

                result_user = await session.execute(select(User).where(User.id == project.user_id))
                user_to_assign = result_user.scalar_one_or_none()
                if not user_to_assign:
                    print(f"Пользователь {project.user_id} не найден.")
                    return False

                result_assignment = await session.execute(
                    select(user_project).where(user_project.c.project_id == project.id,
                                               user_project.c.user_id == project.user_id)
                )
                existing_assignment = result_assignment.fetchone()
                if existing_assignment:
                    print(f"Пользователь {project.user_id} уже назначен на проект {project.id}.")
                    return False

                await session.execute(
                    insert(user_project).values(project_id=project.id, user_id=project.user_id)
                )
                await session.commit()
                return True
            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Ошибка базы данных при добавлении пользователя к проекту: {e}")
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Неожиданная ошибка при добавлении пользователя к проекту: {e}")

    @classmethod
    async def get_assigned_users(cls, project: AssignedUsers) -> List[OutputAssignedUsers]:
        async with new_session() as session:
            try:
                result = await session.execute(
                    select(user_project.c.user_id).where(user_project.c.project_id == project.id)
                )
                assigned_users = result.fetchall()
                output_assigned_users = [
                    OutputAssignedUsers(user_id=user_id) for user_id in [user[0] for user in assigned_users]
                ]
                return output_assigned_users
            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Ошибка базы данных при получении пользователей, привязанных к проекту: {e}")
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Неожиданная ошибка при получении пользователей, привязанных к проекту: {e}")
