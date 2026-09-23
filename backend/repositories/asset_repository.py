from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.asset import Asset


class AssetRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Asset).all()

    def get_by_id(self, asset_id: int):
        return self.db.query(Asset).filter(Asset.id == asset_id).first()

    def get_by_asset_id(self, asset_id: str):
        return self.db.query(Asset).filter(Asset.asset_id == asset_id).first()

    def create(self, asset: Asset):
        self.db.add(asset)
        self.db.commit()
        self.db.refresh(asset)
        return asset

    def update(self, asset: Asset):
        self.db.commit()
        self.db.refresh(asset)
        return asset

    def delete(self, asset: Asset):
        self.db.delete(asset)
        self.db.commit()

    def search(self, keyword: str):
        return (
            self.db.query(Asset)
            .filter(
                (Asset.asset_name.ilike(f"%{keyword}%"))
                | (Asset.asset_id.ilike(f"%{keyword}%"))
                | (Asset.cloud_provider.ilike(f"%{keyword}%"))
                | (Asset.owner.ilike(f"%{keyword}%"))
            )
            .all()
        )
