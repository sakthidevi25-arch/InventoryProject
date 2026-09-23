from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AuditLogCreate(BaseModel):
    username: str
    action: str
    entity_type: str
    entity_id: Optional[str] = None
    details: Optional[str] = None


class AuditLogRead(AuditLogCreate):
    id: int
    timestamp: datetime
    user_id: Optional[int] = None

    class Config:
        from_attributes = True
