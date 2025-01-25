import uuid
from datetime import datetime, timedelta
from typing import Optional

from fastapi.params import Depends
from jose import jwt
from loguru import logger
from pydantic import EmailStr, UUID4

from solution.app.config import settings
from solution.app.database import async_session_maker
from solution.app.exceptions import UserExistsException, UserGetException, UserNotFoundException, UserUpdateException
from solution.app.user.dao import UserDAO
from solution.app.user.models import UserModel
from solution.app.user.schemas import UserCreate, UserCreateDB, User, UserUpdateDB
from solution.app.utils import get_password_hash, is_valid_password


class UserService:
    @classmethod
    async def register_new_user(cls, user: UserCreate) -> UserModel:
        try:
            async with async_session_maker() as session:
                user_exist = await UserDAO.find_one_or_none(session, email=user.email)
        except Exception as e:
            logger.error(f"Failed register new user with details {user} ---> Error: {str(e)}")
            raise UserGetException

        if user_exist:
            logger.error(f"Failed register new user with details {user} ---> User already exists")
            raise UserExistsException

        db_user = await UserDAO.add(session,
                                    UserCreateDB(**user.model_dump(), hashed_password=get_password_hash(user.password)))
        await session.commit()

        logger.info(f"New user {db_user.id} successful registered")
        return db_user

    @classmethod
    async def authenticate_user(cls, email: EmailStr, password: str) -> Optional[UserModel]:
        async with async_session_maker() as session:
            db_user = await UserDAO.find_one_or_none(session, email=email)
        if db_user and is_valid_password(password, db_user.hashed_password):
            logger.info(f"User {db_user.id} successful authenticated")
            return db_user
        return None

    @classmethod
    async def create_token(cls, user_id: uuid.UUID) -> str:
        access_token = cls._create_access_token(user_id)
        return access_token

    @classmethod
    def _create_access_token(cls, user_id: uuid.UUID) -> str:
        to_encode = {
            "sub": str(user_id),
            "exp": datetime.utcnow() + timedelta(
                minutes=720)
        }
        encoded_jwt = jwt.encode(
            to_encode, settings.RANDOM_SECRET, algorithm="HS256")
        return f'Bearer {encoded_jwt}'

    @classmethod
    async def get_user(cls, user_id) -> UserModel:
        try:
            async with async_session_maker() as session:
                user = await UserDAO.find_one_or_none(session, id=user_id)
        except Exception as e:
            logger.error(f"Failed get user {user_id} ---> Error: {str(e)}")
            raise UserGetException
        if user is None:
            logger.error(f"User {user_id} not found")
            raise UserNotFoundException
        logger.info(f"Found user {user.id}")
        return user

    @classmethod
    async def update_user(cls, user_id: UUID4, new_user: UserCreate, user: User = Depends(get_user)):
        if user:
            try:
                async with async_session_maker() as session:
                    db_user = await UserDAO.update(session, UserModel.id == user_id,
                                                   obj_in=UserUpdateDB(**new_user.model_dump(),
                                                                       hashed_password=get_password_hash(
                                                                           new_user.password)))
                    await session.commit()
            except Exception as e:
                logger.error(f"Failed update user {user_id} ---> Error: {str(e)}")
                raise UserUpdateException

            return db_user
