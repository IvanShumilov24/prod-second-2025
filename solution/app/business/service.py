import uuid
from datetime import datetime, timedelta

from jose import jwt
from loguru import logger
from pydantic import EmailStr
from typing_extensions import Optional

from solution.app.business.dao import BusinessDAO
from solution.app.business.models import BusinessModel
from solution.app.business.schemas import BusinessCreate, BusinessCreateDB
from solution.app.config import settings
from solution.app.database import async_session_maker
from solution.app.exceptions import BusinessExistsException
from solution.app.utils import get_password_hash, is_valid_password


class BusinessService:

    @classmethod
    async def register_new_business(cls, business: BusinessCreate) -> BusinessModel:
        try:
            async with async_session_maker() as session:
                business_exist = await BusinessDAO.find_one_or_none(session, email=business.email)
        except Exception as e:
            logger.error(f"Failed register new business with details {business} ---> Error: {str(e)}")
        if business_exist:
            logger.error(f"Failed register new business with details {business} ---> Business already exists")
            raise BusinessExistsException
        db_business = await BusinessDAO.add(
            session,
            BusinessCreateDB(
                **business.model_dump(),
                hashed_password=get_password_hash(business.password))
        )
        await session.commit()

        logger.info(f"New business successful registered with details {business}")
        return db_business

    @classmethod
    async def authenticate_business(cls, email: EmailStr, password: str) -> Optional[BusinessModel]:
        async with async_session_maker() as session:
            db_business = await BusinessDAO.find_one_or_none(session, email=email)
        if db_business and is_valid_password(password, db_business.hashed_password):
            logger.info("Business successful authenticated")
            return db_business
        return None

    @classmethod
    async def create_token(cls, business_id: uuid.UUID) -> str:
        access_token = cls._create_access_token(business_id)
        return access_token

    @classmethod
    def _create_access_token(cls, business_id: uuid.UUID) -> str:
        to_encode = {
            "sub": str(business_id),
            "exp": datetime.utcnow() + timedelta(
                minutes=720)
        }
        encoded_jwt = jwt.encode(
            to_encode, settings.RANDOM_SECRET, algorithm="HS256")
        return f'Bearer {encoded_jwt}'

    @classmethod
    async def get_business(cls, business_id: uuid.UUID) -> BusinessModel:
        async with async_session_maker() as session:
            business = await BusinessDAO.find_one_or_none(session, id=business_id)
        if business is None:
            logger.error(f"Business with id {business_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Business not found")
        logger.info(f"Business with id {business_id} found")
        return business
