from __future__ import annotations

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.base import Base


class Api(Base):
    __tablename__ = "apis"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    api_name: Mapped[str] = mapped_column(String(255), nullable=False)
    api_path: Mapped[str] = mapped_column(String(500), nullable=False)
    http_method: Mapped[str] = mapped_column(String(20), nullable=False)
    application_name: Mapped[str] = mapped_column(String(255), nullable=False)
    owner: Mapped[str] = mapped_column(String(150), nullable=False)
    environment: Mapped[str] = mapped_column(String(50), nullable=False)
    authentication_type: Mapped[str] = mapped_column(String(80), nullable=False)
    version: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
