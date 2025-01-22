from loguru import logger

from solution.app.business.schemas import Business
from solution.app.database import async_session_maker
from solution.app.exceptions import PromoCreationException
from solution.app.promo.dao import PromoDAO
from solution.app.promo.schemas import PromoCreate, PromoCreateDB


class PromoService:
    @classmethod
    async def create(cls, promo: PromoCreate, business: Business):
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
