from typing import TypeVar, Type

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, model: Type[ModelType]):
        return self.db.query(model).all()

    def get_by_id(self, model: Type[ModelType], item_id: int):
        return self.db.query(model).filter(model.id == item_id).first()

    def delete(self, obj):
        self.db.delete(obj)
        self.db.commit()
