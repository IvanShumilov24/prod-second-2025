from solution.app.promo.models import PromoModel
from solution.app.promo.schemas import PromoCreate, PromoUpdate


class PromoDAO(BaseDAO[PromoModel, PromoCreate, PromoUpdate]):
    model = PromoModel
