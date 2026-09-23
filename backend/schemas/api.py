from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class ApiBase(BaseModel):
    api_name: str = Field(..., min_length=2, max_length=255)
    api_path: str = Field(..., min_length=1, max_length=500)
    http_method: str = Field(..., min_length=2, max_length=20)
    application_name: str = Field(..., min_length=2, max_length=255)
    owner: str = Field(..., min_length=2, max_length=150)
    environment: str = Field(..., min_length=2, max_length=50)
    authentication_type: str = Field(..., min_length=2, max_length=80)
    version: str = Field(..., min_length=1, max_length=30)
    description: Optional[str] = None


class ApiCreate(ApiBase):
    pass


class ApiUpdate(ApiBase):
    pass


class ApiRead(ApiBase):
    id: int

    class Config:
        from_attributes = True
