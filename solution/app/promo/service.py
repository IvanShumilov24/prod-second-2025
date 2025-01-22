from typing import Literal

from loguru import logger
from pydantic import UUID4

from solution.app.business.schemas import Business
from solution.app.database import async_session_maker
from solution.app.exceptions import PromoCreationException, PromoGetException, PromoNotFoundException, \
    PromoNotBelongBusinessException
from solution.app.promo.dao import PromoDAO
from solution.app.promo.models import PromoModel
from solution.app.promo.schemas import PromoCreate, PromoCreateDB
from solution.app.promo.utils import sort_promo_list


class PromoService:
    @classmethod
    async def create_promo(cls, promo: PromoCreate, business: Business) -> UUID4:
        try:
            async with async_session_maker() as session:
                db_promo = await PromoDAO.add(session, PromoCreateDB(**promo.model_dump(), company_id=business.id,
                                                                     company_name=business.name))
                await session.commit()
        except Exception as e:
            logger.error(f"Failed create promo with details: {promo} ---> Error: {str(e)}")
            raise PromoCreationException

        logger.info(f"New promo successful created with details {promo}")
        return db_promo.promo_id

    @classmethod
    async def get_all_promo_by_business(cls, business: Business, limit: int, offset: int,
                                        sort_by: Literal["active_from", "active_until"], ) -> list[PromoModel]:
        try:
            async with async_session_maker() as session:
                promo_list = await PromoDAO.find_all(session, limit=limit, offset=offset, company_id=business.id)
        except Exception as e:
            logger.error(f"Failed get promo by business {business.id} ---> Error {str(e)}")
            raise PromoGetException

        sort_promo_list(promo_list, sort_by)
        logger.info(f"Found {len(promo_list)} promo by business {business.id}")
        return promo_list

    @classmethod
    async def get_promo(cls, promo_id: UUID4, business: Business) -> PromoModel:
        try:
            async with async_session_maker() as session:
                promo = await PromoDAO.find_one_or_none(session, promo_id=promo_id)
        except Exception as e:
            logger.error(f"Failed get promo {promo_id} by business {business.id} ---> Error {str(e)}")
            raise PromoGetException
        if not promo:
            logger.error(f"Not found promo {promo_id} by business {business.id}")
            raise PromoNotFoundException
        elif promo.company_id != business.id:
            raise PromoNotBelongBusinessException
        logger.info(f"Found promo {promo_id}")
        return promo
