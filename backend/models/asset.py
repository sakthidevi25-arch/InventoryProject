from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.base import Base


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    asset_id: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    asset_name: Mapped[str] = mapped_column(String(255), nullable=False)
    asset_category: Mapped[str] = mapped_column(String(100), nullable=False)
    cloud_provider: Mapped[str] = mapped_column(String(100), nullable=False)
    account_id: Mapped[str] = mapped_column(String(100), nullable=False)
    region: Mapped[str] = mapped_column(String(100), nullable=False)
    owner: Mapped[str] = mapped_column(String(150), nullable=False)
    environment: Mapped[str] = mapped_column(String(50), nullable=False)
    criticality: Mapped[str] = mapped_column(String(50), nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
