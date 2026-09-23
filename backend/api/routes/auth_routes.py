from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.models.user import User
from backend.repositories.user_repository import UserRepository
from backend.schemas.user import Token, UserCreate, UserLogin, UserPasswordChange, UserPasswordResetRequest
from backend.security.jwt_handler import get_token_payload
from backend.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    user = service.register(payload)
    return {"message": "User registered successfully", "user_id": user.id, "username": user.username}


@router.post("/login", response_model=dict)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    service = AuthService(db)
    token, user = service.login(payload)
    return {"access_token": token, "token_type": "bearer", "user": {"id": user.id, "username": user.username, "email": user.email}}


@router.post("/change-password")
def change_password(payload: UserPasswordChange, token_payload: dict = Depends(get_token_payload), db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(int(token_payload["sub"]))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    service = AuthService(db)
    service.change_password(user, payload.current_password, payload.new_password)
    return {"message": "Password changed successfully"}


@router.post("/forgot-password")
def forgot_password(payload: UserPasswordResetRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.forgot_password(payload.email)
