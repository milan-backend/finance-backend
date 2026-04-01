from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models import User, RefreshToken

from app.core.hashing import hash_password, verify_password
from app.core.security import create_access_token
from app.core.tokens import generate_refresh_token, get_refresh_token_expiry
from app.schemas import RegisterRequest, RefreshRequest
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=data.email,
        password=hash_password(data.password),
        role="viewer"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered successfully"}



@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    #  username = email
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token({
        "user_id": user.id,
        "role": user.role
    })

    refresh_token_str = generate_refresh_token()
    expires_at = get_refresh_token_expiry()

    refresh_token = RefreshToken(
        token=refresh_token_str,
        user_id=user.id,
        expires_at=expires_at
    )

    db.add(refresh_token)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token_str,
        "token_type": "bearer"
    }




@router.post("/refresh")
def refresh_token(data: RefreshRequest, db: Session = Depends(get_db)):

    token_entry = db.query(RefreshToken)\
        .filter(RefreshToken.token == data.refresh_token)\
        .first()

    if not token_entry:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if token_entry.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token expired")

    user = token_entry.user

    new_access_token = create_access_token({
        "user_id": user.id,
        "role": user.role
    })

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }