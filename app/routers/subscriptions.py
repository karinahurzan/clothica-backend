from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, database


router = APIRouter()


@router.post("/")
def subscribe(
    email: schemas.SubscriptionCreate, db: Session = Depends(database.get_db)
):
    new_sub = models.Subscription(email=email.email)
    db.add(new_sub)
    db.commit()
    return {"message": "Subscribed successfully"}
