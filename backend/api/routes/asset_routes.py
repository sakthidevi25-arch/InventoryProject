from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.models.user import User
from backend.schemas.asset import AssetCreate, AssetRead, AssetUpdate
from backend.services.asset_service import AssetService
from backend.security.jwt_handler import get_token_payload

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.get("/", response_model=list[AssetRead])
def list_assets(db: Session = Depends(get_db), _: dict = Depends(get_token_payload)):
    service = AssetService(db)
    return service.get_assets()


@router.get("/search", response_model=list[AssetRead])
def search_assets(keyword: str = Query(default=""), db: Session = Depends(get_db), _: dict = Depends(get_token_payload)):
    service = AssetService(db)
    return service.search_assets(keyword)


@router.get("/{asset_id}", response_model=AssetRead)
def get_asset(asset_id: int, db: Session = Depends(get_db), _: dict = Depends(get_token_payload)):
    service = AssetService(db)
    return service.get_asset_by_id(asset_id)


@router.post("/", response_model=AssetRead)
def create_asset(payload: AssetCreate, db: Session = Depends(get_db), _: dict = Depends(get_token_payload)):
    service = AssetService(db)
    return service.create_asset(payload)


@router.put("/{asset_id}", response_model=AssetRead)
def update_asset(asset_id: int, payload: AssetUpdate, db: Session = Depends(get_db), _: dict = Depends(get_token_payload)):
    service = AssetService(db)
    return service.update_asset(asset_id, payload)


@router.delete("/{asset_id}")
def delete_asset(asset_id: int, db: Session = Depends(get_db), _: dict = Depends(get_token_payload)):
    service = AssetService(db)
    return service.delete_asset(asset_id)
