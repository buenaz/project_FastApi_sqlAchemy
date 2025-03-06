from typing import Any, Optional

from fastapi import HTTPException, status
from sqlalchemy import select, delete, update
from sqlalchemy.exc import SQLAlchemyError

from profiles.profile_models import ProfileDelete, ProfileAdd, OutputProfileGet, ProfileGet, ProfileUpdate
from db import User, Profile, Project, Task, new_session


class ProfileRequests:
    @classmethod
    async def add_profile(cls, profile: ProfileAdd) -> int:
        async with new_session() as session:
            try:
                data = profile.model_dump()
                new_profile = Profile(**data)
                session.add(new_profile)
                await session.flush()
                await session.commit()
                return new_profile.user_id
            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Ошибка базы данных при добавлении профиля: {e}")
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Неожиданная ошибка при добавлении профиля: {e}")

    @classmethod
    async def get_profile(cls, profile: ProfileGet) -> Optional[OutputProfileGet]:
        async with new_session() as session:
            try:
                result = await session.execute(select(Profile).where(Profile.user_id == profile.user_id))
                profile_to_get = result.scalar_one_or_none()
                if profile_to_get:
                    return OutputProfileGet.model_validate(profile_to_get)
                else:
                    print(f"Профиль пользователя с user_id {profile.user_id} не найден.")
                    return None
            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Ошибка базы данных при получении профиля: {e}")
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Неожиданная ошибка при получении профиля: {e}")

    @classmethod
    async def delete_profile(cls, profile: ProfileDelete) -> bool:
        async with new_session() as session:
            try:
                result = await session.execute(select(Profile).where(Profile.user_id == profile.user_id))
                profile_to_delete = result.scalar_one_or_none()
                if profile_to_delete:
                    await session.delete(profile_to_delete)
                    await session.commit()
                    return True
                else:
                    print(f"Пользователь с id {profile.user_id} не найден.")
                    return False
            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Ошибка базы данных при удалении профиля: {e}")
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Неожиданная ошибка при удалении профиля: {e}")

    @classmethod
    async def update_profile(cls, profile: ProfileUpdate) -> bool:
        async with new_session() as session:
            try:
                profile_to_update = await session.execute(select(Profile).where(Profile.id == profile.id))
                profile_to_update = profile_to_update.scalar_one_or_none()

                if not profile_to_update:
                    print(f"Профиль с ID {profile.id} не найден")
                    return False

                update_values = {}

                if profile.bio:
                    update_values["bio"] = profile.bio
                if profile.phone:
                    update_values["phone"] = profile.phone
                if profile.skill:
                    update_values["skill"] = profile.skill
                if profile.social_link:
                    update_values["social_link"] = profile.social_link

                if update_values:
                    await session.execute(update(Profile).where(Profile.user_id == profile.user_id).values(update_values))
                    await session.commit()
                    return True
                else:
                    return True
            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Ошибка базы данных при обновлении профиля: {e}")
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Неожиданная ошибка при обновлении профиля: {e}")
