from fastapi import HTTPException, status
from sqlalchemy import select, delete, update
from sqlalchemy.exc import SQLAlchemyError

from users.user_models import UserAdd, ConfigUser, UserDelete, UpdateUser
from db import User, Profile, new_session


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
            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Ошибка базы данных при добавлении пользователя: {e}")
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Неожиданная ошибка при добавлении пользователя: {e}")

    @classmethod
    async def get_users(cls) -> list[ConfigUser]:
        async with new_session() as session:
            try:
                result = await session.execute(select(User))
                user_models = result.scalars().all()
                return [ConfigUser.model_validate(user_model) for user_model in user_models]
            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Ошибка базы данных при получении пользователя: {e}")
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Неожиданная ошибка при получении пользователя: {e}")

    @classmethod
    async def delete_user(cls, user: UserDelete) -> bool:
        async with new_session() as session:
            try:
                result_user = await session.execute(select(User).where(User.id == user.id))
                user_to_delete = result_user.scalar_one_or_none()

                if not user_to_delete:
                    print(f"Пользователь с id {user.id} не найден.")
                    return False

                result_profile = await session.execute(select(Profile).where(Profile.user_id == user.id))
                profile_to_delete = result_profile.scalar_one_or_none()

                if profile_to_delete:
                    await session.delete(profile_to_delete)
                await session.delete(user_to_delete)

                await session.commit()
                return True
            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Ошибка базы данных при удалении пользователя: {e}")
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Неожиданная ошибка при удалении пользователя: {e}")

    @classmethod
    async def update_user(cls, user: UpdateUser) -> bool:
        async with new_session() as session:
            try:
                user_to_update = await session.execute(select(User).where(User.id == user.id))
                user_to_update = user_to_update.scalar_one_or_none()

                if not user_to_update:
                    print(f"Пользователь с id {user.id} не найден.")
                    return False

                update_values = {}

                if user.email:
                    update_values["email"] = user.email
                if user.username:
                    update_values["username"] = user.username
                if user.role:
                    update_values["role"] = user.role

                if update_values:
                    await session.execute(update(User).where(User.id == user.id).values(update_values))
                    await session.commit()
                    return True
                else:
                    return True
            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Ошибка базы данных при обновлении пользователя: {e}")
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Неожиданная ошибка при обновлении пользователя: {e}")
