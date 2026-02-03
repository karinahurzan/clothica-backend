from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database
from ..security import get_current_user, get_admin_user


router = APIRouter()


@router.post("/", status_code=201)
def place_order(
    order: schemas.OrderCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_order = models.Order(**order.dict(), user_id=current_user.id)
    db.add(new_order)
    db.commit()
    return {"message": "Order created", "id": new_order.id}


@router.get("/my", response_model=List[schemas.OrderOut])
def get_my_orders(current_user: models.User = Depends(get_current_user)):
    return current_user.orders


def change_order_status(
    order_id: int,
    status: str,
    db: Session = Depends(database.get_db),
    admin: models.User = Depends(get_admin_user),
):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    order.status = status
    db.commit()
    return {"message": "Status updated"}
