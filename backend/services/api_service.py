from __future__ import annotations

from fastapi import HTTPException, status

from backend.models.api import Api
from backend.repositories.api_repository import ApiRepository


class ApiService:
    def __init__(self, db):
        self.db = db
        self.repo = ApiRepository(db)

    def create_api(self, payload):
        api_obj = Api(**payload.model_dump())
        return self.repo.create(api_obj)

    def get_apis(self):
        return self.repo.get_all()

    def get_api_by_id(self, api_id: int):
        api_obj = self.repo.get_by_id(api_id)
        if not api_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API not found")
        return api_obj

    def update_api(self, api_id: int, payload):
        api_obj = self.repo.get_by_id(api_id)
        if not api_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API not found")
        for key, value in payload.model_dump().items():
            setattr(api_obj, key, value)
        return self.repo.update(api_obj)

    def delete_api(self, api_id: int):
        api_obj = self.repo.get_by_id(api_id)
        if not api_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API not found")
        self.repo.delete(api_obj)
        return {"message": "API deleted successfully"}

    def search_apis(self, keyword: str):
        if not keyword:
            return self.repo.get_all()
        return self.repo.search(keyword)
