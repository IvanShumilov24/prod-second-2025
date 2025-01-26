from app.dao import BaseDAO
from app.promo.models import PromoModel
from app.promo.schemas import PromoCreateDB, PromoUpdate


class PromoDAO(BaseDAO[PromoModel, PromoCreateDB, PromoUpdate]):
    model = PromoModel
