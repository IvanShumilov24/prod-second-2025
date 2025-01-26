from typing import Literal

from app.promo.dao import PromoDAO
from app.promo.models import PromoModel
from app.promo.schemas import PromoCreate, PromoCreateDB, PromoUpdate, Promo, PromoForUser, Target
from fastapi.params import Depends
from loguru import logger
from pydantic import UUID4
from pydantic_extra_types.country import CountryAlpha2

from app.business.schemas import Business
from app.database import async_session_maker
from app.exceptions import PromoCreationException, PromoGetException, PromoNotFoundException, \
    PromoNotBelongBusinessException
from app.utils import sort_promo_list
from starlette.routing import websocket_session


class PromoService:
    @classmethod
    async def create_promo(cls, business: Business, promo: PromoCreate) -> UUID4:
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
    async def get_all_promo(cls, business: Business, limit: int, offset: int,
                            sort_by: Literal["active_from", "active_until"], ) -> list[PromoModel]:
        try:
            async with async_session_maker() as session:
                promo_list = await PromoDAO.find_all(session, limit=limit, offset=offset, company_id=business.id)
        except Exception as e:
            logger.error(f"Failed get promo by business {business.id} ---> Error: {str(e)}")
            raise PromoGetException

        sort_promo_list(promo_list, sort_by)
        logger.info(f"Found {len(promo_list)} promo by business {business.id}")
        return promo_list

    @classmethod
    async def get_promo(cls, business: Business, promo_id: UUID4) -> PromoModel:
        try:
            async with async_session_maker() as session:
                promo = await PromoDAO.find_one_or_none(session, promo_id=promo_id)
        except Exception as e:
            logger.error(f"Failed get promo {promo_id} by business {business.id} ---> Error: {str(e)}")
            raise PromoGetException
        if not promo:
            logger.error(f"Not found promo {promo_id} by business {business.id}")
            raise PromoNotFoundException
        elif promo.company_id != business.id:
            raise PromoNotBelongBusinessException
        logger.info(f"Found promo {promo_id}")
        return promo

    @classmethod
    async def update_promo(cls, business: Business, promo_id: UUID4, new_promo: PromoUpdate,
                           promo: Promo = Depends(get_promo)) -> PromoModel:
        if promo:
            try:
                async with async_session_maker() as session:
                    db_promo = await PromoDAO.update(session, PromoModel.promo_id == promo_id, obj_in=new_promo)
                    await session.commit()
            except Exception as e:
                logger.error(f"Failed update promo {promo_id} by business {business.id} ---> Error: {str(e)}")
                raise PromoGetException

            logger.info(f"Promo {promo_id} successful update by business {business.id}")
            return db_promo

    @classmethod
    async def get_all_promo_by_user(cls, active: bool | None, limit: int = 10, offset: int = 0, category: str = None) -> \
            list[PromoForUser]:
        try:
            async with async_session_maker() as session:
                if active is None:
                    promo_list = await PromoDAO.find_all(session, limit=limit, offset=offset)
                else:
                    promo_list = await PromoDAO.find_all(session, limit=limit, offset=offset, active=active)
        except Exception as e:
            logger.error(f"Failed get all promo ---> Error: {str(e)}")
            raise PromoGetException
        if category:
            promo_list = [promo for promo in promo_list if category in promo.target["categories"]]
        logger.info(f"Found {len(promo_list)} promo")
        return [PromoForUser(description=promo.description,
                             image_url=promo.image_url,
                             target=Target(age_from=promo.target['age_from'],
                                           age_until=promo.target['age_until'],
                                           country=CountryAlpha2(promo.target["country"]),
                                           categories=promo.target["categories"]),
                             max_count=promo.max_count,
                             active_from=promo.active_from,
                             active_until=promo.active_until,
                             promo_id=promo.promo_id,
                             company_id=promo.company_id,
                             company_name=promo.company_name,
                             active=promo.active,
                             like_count=promo.like_count,
                             is_activated_by_user=False,
                             is_liked_by_user=False,
                             comment_count=0) for promo in promo_list]

    @classmethod
    async def get_promo_by_user(cls, promo_id) -> PromoForUser:
        try:
            async with async_session_maker() as session:
                promo = await PromoDAO.find_one_or_none(session, promo_id=promo_id)
        except Exception as e:
            logger.error(f"Failed get promo {promo_id} ---> Error: {str(e)}")
            raise PromoGetException
        if not promo:
            logger.error(f"Not found promo {promo_id}")
            raise PromoNotFoundException
        logger.info(f"Found promo {promo_id}")
        return PromoForUser(description=promo.description,
                            image_url=promo.image_url,
                            target=Target(age_from=promo.target['age_from'],
                                          age_until=promo.target['age_until'],
                                          country=CountryAlpha2(promo.target["country"]),
                                          categories=promo.target["categories"]),
                            max_count=promo.max_count,
                            active_from=promo.active_from,
                            active_until=promo.active_until,
                            promo_id=promo.promo_id,
                            company_id=promo.company_id,
                            company_name=promo.company_name,
                            active=promo.active,
                            like_count=promo.like_count,
                            is_activated_by_user=False,
                            is_liked_by_user=False,
                            comment_count=0)

    @classmethod
    async def like_promo(cls, promo_id) -> None:
        try:
            async with async_session_maker() as session:
                promo = await PromoDAO.find_one_or_none(session, promo_id=promo_id)
        except Exception as e:
            logger.error(f"Failed get promo {promo_id} ---> Error: {str(e)}")
            raise PromoGetException
        if not promo:
            logger.error(f"Not found promo {promo_id}")
            raise PromoNotFoundException



        logger.info(f"Promo {promo_id} successful liked")
        return None

    # @classmethod
    # async def delete_like_promo(cls, promo_id) -> None:
    #     try:
    #         async with async_session_maker() as session:
    #             promo = await PromoDAO.find_one_or_none(session, promo_id=promo_id)
    #     except Exception as e:
    #         logger.error(f"Failed get promo {promo_id} ---> Error: {str(e)}")
    #         raise PromoGetException
    #     if not promo:
    #         logger.error(f"Not found promo {promo_id}")
    #         raise PromoNotFoundException
    #
    #     try:
    #         async with async_session_maker() as session:
    #             db_promo = await PromoDAO.update(session, promo_id=promo_id)
    #
    #     logger.info(f"Like promo {promo_id} successful delete")
    #     return None