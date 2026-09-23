from __future__ import annotations

from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.core.config import settings
from backend.models.role import Role
from backend.models.user import User
from backend.repositories.audit_repository import AuditRepository
from backend.repositories.user_repository import UserRepository
from backend.schemas.user import UserCreate, UserLogin
from backend.security.jwt_handler import create_access_token
from backend.security.password_utils import hash_password, verify_password


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.audit_repo = AuditRepository(db)

    def register(self, user_data: UserCreate):
        if self.user_repo.get_by_username(user_data.username):
            raise HTTPException(status_code=400, detail="Username already registered")
        if self.user_repo.get_by_email(user_data.email):
            raise HTTPException(status_code=400, detail="Email already registered")

        role_name = user_data.role_name or "User"
        role = self.user_repo.get_role_by_name(role_name)
        if not role:
            role = Role(name=role_name, description=f"{role_name} role")
            self.db.add(role)
            self.db.commit()
            self.db.refresh(role)

        user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            password_hash=hash_password(user_data.password),
            role_id=role.id,
            is_active=True,
            is_verified=True,
        )
        self.user_repo.create(user)
        return user

    def login(self, login_data: UserLogin):
        user = self.user_repo.get_by_username(login_data.username)
        if not user or not verify_password(login_data.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account disabled")

        user.last_login = datetime.utcnow()
        self.user_repo.update(user)

        role_name = user.role.name if user.role else "User"
        token = create_access_token(
            subject=str(user.id),
            username=user.username,
            role=role_name,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        return token, user

    def change_password(self, user: User, current_password: str, new_password: str):
        if not verify_password(current_password, user.password_hash):
            raise HTTPException(status_code=400, detail="Current password is incorrect")
        user.password_hash = hash_password(new_password)
        self.user_repo.update(user)
        return True

    def forgot_password(self, email: str):
        user = self.user_repo.get_by_email(email)
        if not user:
            return {"message": "If an account exists, a reset email has been sent."}
        user.reset_token = "mock-reset-token" 
        user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
        self.user_repo.update(user)
        return {"message": "Password reset instructions have been sent."}
