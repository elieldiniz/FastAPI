from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.user_repo import user_repo
from app.models.user import User
from app.core.security import verify_password

class AuthService:
    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        user = user_repo.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_admin(self, user: User) -> bool:
        return user.role == "admin"

auth_service = AuthService()
