from typing import Any, Optional

from sqlalchemy import select, delete, update
from models import (UserAdd, ConfigUser, UserDelete, UpdateUserEmail, ProfileDelete,
                    ProfileAdd, OutputProfileGet, ProfileGet, ProfileUpdate)
from db import User, Profile, Project, Task, new_session


class UserRequests:
    @classmethod
    async def add_user(cls, user: UserAdd) -> int:
        async with new_session() as session:
            try:
                data = user.model_dump()
                new_user = User(**data)
                session.add(new_user)
                await session.flush()
                await session.commit()
                return new_user.id
            except Exception as e:
                print(f"Ошибка при добавлении пользователя: {e}")
                await session.rollback()

    @classmethod
    async def get_users(cls) -> list[ConfigUser]:
        async with new_session() as session:
            try:
                result = await session.execute(select(User))
                user_models = result.scalars().all()
                return [ConfigUser.model_validate(user_model) for user_model in user_models]
            except Exception as e:
                print(f"Ошибка при получении пользователей: {e}")
                await session.rollback()

    @classmethod
    async def delete_user(cls, user: UserDelete) -> None:
        async with new_session() as session:
            try:
                result_user = await session.execute(select(User).where(User.id == user.id))
                result_profile = await session.execute(select(Profile).where(Profile.user_id == user.id))
                user_to_delete = result_user.scalar_one_or_none()
                profile_to_delete = result_profile.scalar_one_or_none()
                if user_to_delete:
                    if profile_to_delete:
                        await session.delete(user_to_delete)
                        await session.delete(profile_to_delete)
                        await session.commit()
                    else:
                        await session.delete(user_to_delete)
                        await session.commit()
                else:
                    print(f"Пользователь с id {user.id} не найден.")
            except Exception as e:
                print(f"Ошибка при удалении пользователя с id {user.id}: {e}")
                await session.rollback()

    @classmethod
    async def update_user_email(cls, user: UpdateUserEmail) -> None:
        async with new_session() as session:
            try:
                await session.execute(update(User).where(User.id == user.id).values(email=user.email))
                await session.commit()
            except Exception as e:
                print(f"Ошибка при изменении email пользователя: {e}")
                await session.rollback()


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
