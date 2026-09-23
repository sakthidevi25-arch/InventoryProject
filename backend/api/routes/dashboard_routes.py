from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.security.jwt_handler import get_token_payload
from backend.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/")
def dashboard(db: Session = Depends(get_db), _: dict = Depends(get_token_payload)):
    service = DashboardService(db)
    return service.get_dashboard()
