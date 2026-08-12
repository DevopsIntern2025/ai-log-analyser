from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.user_schema import UserCreate


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def register_user(
    db: Session,
    user_data: UserCreate,
) -> User:

    existing_user = get_user_by_email(
        db,
        user_data.email,
    )

    if existing_user:
        raise ValueError("Email already registered")

    hashed_password = hash_password(
        user_data.password
    )

    user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hashed_password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:

    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(
        password,
        user.hashed_password,
    ):
        return None

    return user


def create_user_token(user: User) -> str:
    return create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
        }
    )