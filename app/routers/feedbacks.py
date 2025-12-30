from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, database


router = APIRouter()


@router.post("/")
def create_feedback(
    feedback: schemas.FeedbackCreate, db: Session = Depends(database.get_db)
):
    new_fb = models.Feedback(**feedback.dict())
    db.add(new_fb)
    db.commit()
    return {"message": "Feedback added"}


@router.get("/{product_id}")
def get_product_feedbacks(product_id: str, db: Session = Depends(database.get_db)):
    return (
        db.query(models.Feedback).filter(models.Feedback.product_id == product_id).all()
    )
