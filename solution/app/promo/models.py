import uuid
from datetime import datetime
from typing import Dict

from sqlalchemy import UUID, JSON, String, ForeignKey, Enum, DATETIME
from sqlalchemy.orm import Mapped, mapped_column

from solution.app.database import Base
from solution.app.promo.schemas import PromoMode


class PromoModel(Base):
    __tablename__ = 'promo'

    description: Mapped[str] = mapped_column(String(300))
    image_url: Mapped[str] = mapped_column(String(350))
    target: Mapped[Dict[str, int]] = mapped_column(JSON)
    max_count: Mapped[int]
    active_from: Mapped[datetime] = mapped_column(DATETIME)
    active_until: Mapped[datetime] = mapped_column(DATETIME)
    mode: Mapped[PromoMode] = mapped_column(Enum(PromoMode, name="mode_enum"))
    promo_common: Mapped[str]
    promo_unique: Mapped[list[str]] = mapped_column(JSON)
    promo_id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    company_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey(
        "business.id", ondelete="CASCADE"))
    company_name: Mapped[str] = mapped_column(String(50), ForeignKey(
        "business.name", ondelete="CASCADE"))
    like_count: Mapped[int] = mapped_column(default=0)
    used_count: Mapped[int] = mapped_column(default=0)
    active: Mapped[bool] = mapped_column(default=True)
