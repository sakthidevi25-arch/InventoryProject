from __future__ import annotations

from fastapi import HTTPException, status

from backend.models.asset import Asset
from backend.repositories.asset_repository import AssetRepository


class AssetService:
    def __init__(self, db):
        self.db = db
        self.repo = AssetRepository(db)

    def create_asset(self, payload):
        if self.repo.get_by_asset_id(payload.asset_id):
            raise HTTPException(status_code=400, detail="Asset ID already exists")
        asset = Asset(**payload.model_dump())
        return self.repo.create(asset)

    def get_assets(self):
        return self.repo.get_all()

    def get_asset_by_id(self, asset_id: int):
        asset = self.repo.get_by_id(asset_id)
        if not asset:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
        return asset

    def update_asset(self, asset_id: int, payload):
        asset = self.repo.get_by_id(asset_id)
        if not asset:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
        for key, value in payload.model_dump().items():
            setattr(asset, key, value)
        return self.repo.update(asset)

    def delete_asset(self, asset_id: int):
        asset = self.repo.get_by_id(asset_id)
        if not asset:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
        self.repo.delete(asset)
        return {"message": "Asset deleted successfully"}

    def search_assets(self, keyword: str):
        if not keyword:
            return self.repo.get_all()
        return self.repo.search(keyword)
