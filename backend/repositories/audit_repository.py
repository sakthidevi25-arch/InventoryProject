from __future__ import annotations

from sqlalchemy.orm import Session

from backend.models.audit_log import AuditLog


class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, audit_log: AuditLog):
        self.db.add(audit_log)
        self.db.commit()
        self.db.refresh(audit_log)
        return audit_log

    def get_all(self):
        return self.db.query(AuditLog).order_by(AuditLog.timestamp.desc()).all()

    def get_for_user(self, username: str):
        return self.db.query(AuditLog).filter(AuditLog.username == username).order_by(AuditLog.timestamp.desc()).all()
