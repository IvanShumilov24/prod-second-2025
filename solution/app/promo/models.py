import uuid
from datetime import date
from typing import Dict, Any

from app.promo.schemas import PromoMode
from pydantic import AnyUrl
from sqlalchemy import UUID, JSON, String, ForeignKey, Enum, Date
from sqlalchemy.orm import Mapped, mapped_column
from typing_extensions import Optional

from app.database import Base


class PromoModel(Base):
    __tablename__ = 'promo'

    description: Mapped[str] = mapped_column(String(300))
    image_url: Mapped[AnyUrl] = mapped_column(String(350))
    target: Mapped[Dict[str, Any]] = mapped_column(JSON)
    max_count: Mapped[int]
    active_from: Mapped[Optional[date]] = mapped_column(Date)
    active_until: Mapped[Optional[date]] = mapped_column(Date)
    mode: Mapped[PromoMode] = mapped_column(Enum(PromoMode, name="mode"))
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
