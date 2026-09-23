from __future__ import annotations

from sqlalchemy.orm import Session

from backend.models.api import Api


class ApiRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Api).all()

    def get_by_id(self, api_id: int):
        return self.db.query(Api).filter(Api.id == api_id).first()

    def create(self, api_obj: Api):
        self.db.add(api_obj)
        self.db.commit()
        self.db.refresh(api_obj)
        return api_obj

    def update(self, api_obj: Api):
        self.db.commit()
        self.db.refresh(api_obj)
        return api_obj

    def delete(self, api_obj: Api):
        self.db.delete(api_obj)
        self.db.commit()

    def search(self, keyword: str):
        return (
            self.db.query(Api)
            .filter(
                (Api.api_name.ilike(f"%{keyword}%"))
                | (Api.api_path.ilike(f"%{keyword}%"))
                | (Api.application_name.ilike(f"%{keyword}%"))
                | (Api.owner.ilike(f"%{keyword}%"))
            )
            .all()
        )
