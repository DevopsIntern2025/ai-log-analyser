from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user_schema import (
    TokenResponse,
    UserCreate,
    UserLogin,
)
from app.services.auth_service import (
    authenticate_user,
    create_user_token,
    register_user,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register")
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    try:
        user = register_user(
            db,
            user_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )

    return {
        "message": "User registered successfully",
        "user_id": user.id,
        "email": user.email,
    }


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db,
        user_data.email,
        user_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_user_token(user)

    return {
        "access_token": token,
        "token_type": "bearer",
    }