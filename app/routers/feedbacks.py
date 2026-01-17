from app.security import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from .. import models, schemas, database


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_feedback(
    feedback: schemas.FeedbackCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    try:
        feedback_data = feedback.dict(exclude={"id"})
        new_fb = models.Feedback(**feedback_data)
        db.add(new_fb)
        db.commit()
        db.refresh(new_fb)
        return new_fb
    except Exception as e:
        db.rollback()
        print(f"Error creating feedback: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/latest")
def get_latest_feedbacks(db: Session = Depends(database.get_db)):
    feedbacks = (
        db.query(models.Feedback)
        .options(joinedload(models.Feedback.goods))
        .order_by(models.Feedback.date.desc())
        .limit(12)
        .all()
    )

    return [
        {
            "id": fb.id,
            "author": fb.author,
            "description": fb.description,
            "rate": fb.rate,
            "product_id": fb.product_id,
            "product_name": fb.goods.name if fb.goods else None,
        }
        for fb in feedbacks
    ]


@router.get("/{product_id}")
def get_product_feedbacks(product_id: str, db: Session = Depends(database.get_db)):
    return (
        db.query(models.Feedback).filter(models.Feedback.product_id == product_id).all()
    )
