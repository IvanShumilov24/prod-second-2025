from datetime import datetime
from typing import Literal, Optional

from loguru import logger

from solution.app.promo.schemas import Promo


def sort_promo_list(promo_list: list[Promo], sort_by: Literal["active_from", "active_until"]) -> list[Promo]:
    def get_date(promo: Promo) -> Optional[datetime]:
        if sort_by == 'active_from':
            date_str = promo.active_from
        elif sort_by == "active_until":
            date_str = promo.active_until
        else:
            date_str = None
        if date_str:
            try:
                return datetime.fromisoformat(date_str)
            except ValueError:
                logger.error("Failed sort list promo")
        return None

    return sorted(promo_list, key=get_date)
