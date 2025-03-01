from sqlalchemy import select, delete, update
from users.user_models import UserAdd, ConfigUser, UserDelete, UpdateUserEmail
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
