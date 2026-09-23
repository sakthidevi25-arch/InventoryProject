from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.schemas.api import ApiCreate, ApiRead, ApiUpdate
from backend.security.jwt_handler import get_token_payload
from backend.services.api_service import ApiService

router = APIRouter(prefix="/apis", tags=["APIs"])


@router.get("/", response_model=list[ApiRead])
def list_apis(db: Session = Depends(get_db), _: dict = Depends(get_token_payload)):
    service = ApiService(db)
    return service.get_apis()


@router.get("/search", response_model=list[ApiRead])
def search_apis(keyword: str = Query(default=""), db: Session = Depends(get_db), _: dict = Depends(get_token_payload)):
    service = ApiService(db)
    return service.search_apis(keyword)


@router.get("/{api_id}", response_model=ApiRead)
def get_api(api_id: int, db: Session = Depends(get_db), _: dict = Depends(get_token_payload)):
    service = ApiService(db)
    return service.get_api_by_id(api_id)


@router.post("/", response_model=ApiRead)
def create_api(payload: ApiCreate, db: Session = Depends(get_db), _: dict = Depends(get_token_payload)):
    service = ApiService(db)
    return service.create_api(payload)


@router.put("/{api_id}", response_model=ApiRead)
def update_api(api_id: int, payload: ApiUpdate, db: Session = Depends(get_db), _: dict = Depends(get_token_payload)):
    service = ApiService(db)
    return service.update_api(api_id, payload)


@router.delete("/{api_id}")
def delete_api(api_id: int, db: Session = Depends(get_db), _: dict = Depends(get_token_payload)):
    service = ApiService(db)
    return service.delete_api(api_id)
