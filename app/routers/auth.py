from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from .. import schemas, models, database
from ..security import (
    hash_password,
    verify_password,
    create_access_token,
    oauth2_scheme,
    get_current_user,
)
from google.oauth2 import id_token
from google.auth.transport import requests

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def sign_up(data: schemas.UserCreate, db: Session = Depends(database.get_db)):
    existing_user = (
        db.query(models.User).filter(models.User.email == data.email).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email {data.email} is already taken.",
        )

    new_user = models.User(
        email=data.email,
        full_name=data.full_name,
        hashed_password=hash_password(data.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": str(new_user.id)})
    return {"token": token, "user_id": new_user.id}


@router.post("/login")
def sign_in(data: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong email or password"
        )

    token = create_access_token({"sub": str(user.id)})
    return {
        "token": token,
        "user_email": user.email,
        "id": user.id,
        "is_admin": user.is_admin,
    }


@router.post("/google-login")
def google_auth(token_data: schemas.TokenData, db: Session = Depends(database.get_db)):
    try:
        id_info = id_token.verify_oauth2_token(
            token_data.token, requests.Request(), "YOUR_GOOGLE_CLIENT_ID"
        )
        email = id_info["email"]

        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            user = models.User(
                email=email, full_name=id_info.get("name"), is_verified=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        api_token = create_access_token({"sub": str(user.id)})
        return {"token": api_token}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Google Token")


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    existing_token = (
        db.query(models.BlacklistedToken)
        .filter(models.BlacklistedToken.token == token)
        .first()
    )

    if not existing_token:
        blacklisted_token = models.BlacklistedToken(token=token)
        db.add(blacklisted_token)
        db.commit()

    return {"message": "Successfully logged out"}
