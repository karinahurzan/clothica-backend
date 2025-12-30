from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models, database

router = APIRouter()


@router.get("/", response_model=List[schemas.CategoryOut])
def get_categories(
    skip: int = 0, limit: int = 20, db: Session = Depends(database.get_db)
):
    return db.query(models.Category).offset(skip).limit(limit).all()
