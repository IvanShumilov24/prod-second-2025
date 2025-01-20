import uuid


from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class BusinessModel(Base):
    __tablename__ = "business"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

