from http.client import HTTPException
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


@router.get("/{id}", response_model=schemas.CategoryOut)
def get_category(id: str, db: Session = Depends(database.get_db)):
    category = db.query(models.Category).filter(models.Category.id == id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category
