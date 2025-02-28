from sqlalchemy import select, delete, update
from models import (UserAdd, ConfigUser, UserDelete, UpdateUserEmail, ProfileDelete,
                    ProfileAdd, UpdateBio, UpdatePhone, ConfigProfile, ProfileGet)
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
                query = select(User)
                result = await session.execute(query)
                user_models = result.scalars().all()
                users = [ConfigUser.model_validate(user_model) for user_model in user_models]
                return users
            except Exception as e:
                print(f"Ошибка при получении пользователей: {e}")
                await session.rollback()

    @classmethod
    async def delete_user(cls, user: UserDelete) -> None:
        async with new_session() as session:
            try:
                query_user = select(User).where(User.id == user.id)
                query_profile = select(Profile).where(Profile.user_id == user.id)
                result_user = await session.execute(query_user)
                result_profile = await session.execute(query_profile)
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
                updating = update(User).where(User.id == user.id).values(email=user.email)
                await session.execute(updating)
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
    async def get_profile(cls, profile: ProfileGet) -> ConfigProfile:
        async with new_session() as session:
            try:
                query = select(Profile).where(Profile.user_id == profile.user_id)
                result = await session.execute(query)
                profile_to_get = result.scalar_one_or_none()
                return ConfigProfile.model_validate(profile_to_get)
            except Exception as e:
                print(f"Ошибка при получении профиля пользователя: {e}")
                await session.rollback()

    @classmethod
    async def delete_profile(cls, profile: ProfileDelete) -> None:
        async with new_session() as session:
            try:
                query = select(Profile).where(Profile.user_id == profile.user_id)
                result = await session.execute(query)
                profile_to_delete = result.scalar_one_or_none()
                if profile_to_delete:
                    await session.delete(profile_to_delete)
                    await session.commit()
                else:
                    print(f"Пользователь с id {profile.user_id} не найден.")
            except Exception as e:
                print(f"Ошибка при удалении профиля пользователя: {e}")
                await session.rollback()
