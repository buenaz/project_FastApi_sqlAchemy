from typing import Any, Optional
from sqlalchemy import select, delete, update
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
            except Exception as e:
                print(f"Ошибка при добавлении профиля пользователя: {e}")
                await session.rollback()

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
            except Exception as e:
                print(f"Ошибка при получении профиля пользователя: {e}")
                await session.rollback()

    @classmethod
    async def delete_profile(cls, profile: ProfileDelete) -> None:
        async with new_session() as session:
            try:
                result = await session.execute(select(Profile).where(Profile.user_id == profile.user_id))
                profile_to_delete = result.scalar_one_or_none()
                if profile_to_delete:
                    await session.delete(profile_to_delete)
                    await session.commit()
                else:
                    print(f"Пользователь с id {profile.user_id} не найден.")
            except Exception as e:
                print(f"Ошибка при удалении профиля пользователя: {e}")
                await session.rollback()

    @classmethod
    async def update_profile(cls, profile: ProfileUpdate) -> None:
        async with new_session() as session:
            try:
                if profile.bio:
                    await session.execute(update(Profile).where(Profile.user_id == profile.user_id).values(bio=profile.bio))
                    await session.commit()
                if profile.phone:
                    await session.execute(update(Profile).where(Profile.user_id == profile.user_id).values(phone=profile.phone))
                    await session.commit()
            except Exception as e:
                print(f"Ошибка при обновлении профиля пользователя: {e}")
                await session.rollback()
