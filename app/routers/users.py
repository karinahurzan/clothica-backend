from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, models, security, database

router = APIRouter()


@router.get("/me", response_model=schemas.UserOut)
def get_current_user_info(
    current_user: models.User = Depends(security.get_current_user),
):
    return current_user


@router.patch("/me", response_model=schemas.UserOut)
def update_user_info(
    user_update: schemas.UserUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    for var, value in vars(user_update).items():
        if value is not None:
            setattr(current_user, var, value)
    db.commit()
    db.refresh(current_user)
    return current_user
