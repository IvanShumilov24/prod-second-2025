from solution.app.dao import BaseDAO
from solution.app.promo.models import PromoModel
from solution.app.promo.schemas import PromoCreateDB, PromoUpdate


class PromoDAO(BaseDAO[PromoModel, PromoCreateDB, PromoUpdate]):
    model = PromoModel
