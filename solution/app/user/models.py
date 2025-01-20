from typing import Any
import uuid
from sqlalchemy import String, JSON, UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from app.database import Base


class UserModel(Base):
    __tablename__ = 'user'


    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100))
    surname: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(120))
    avatar_url: Mapped[str] = mapped_column(String(350))
    other: Mapped[dict[str, Any]] = mapped_column(JSON)
