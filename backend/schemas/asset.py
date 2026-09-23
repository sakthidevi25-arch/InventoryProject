from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AssetBase(BaseModel):
    asset_id: str = Field(..., min_length=2, max_length=100)
    asset_name: str = Field(..., min_length=2, max_length=255)
    asset_category: str = Field(..., min_length=2, max_length=100)
    cloud_provider: str = Field(..., min_length=2, max_length=100)
    account_id: str = Field(..., min_length=2, max_length=100)
    region: str = Field(..., min_length=2, max_length=100)
    owner: str = Field(..., min_length=2, max_length=150)
    environment: str = Field(..., min_length=2, max_length=50)
    criticality: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = None


class AssetCreate(AssetBase):
    pass


class AssetUpdate(AssetBase):
    pass


class AssetRead(AssetBase):
    id: int
    created_date: datetime

    class Config:
        from_attributes = True
