from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, database

router = APIRouter()


def format_good(good):
    """Допоміжна функція для пакування ціни в об'єкт"""
    return {
        "id": good.id,
        "name": good.name,
        "category_id": good.category_id,
        "image": good.image,
        "description": good.description,
        "prevDescription": good.prevDescription,
        "gender": good.gender,
        "size": good.size,
        "characteristics": good.characteristics,
        "price": {"value": good.price_value, "currency": good.price_currency},
    }


@router.get("/", response_model=List[schemas.GoodOut])
def get_goods(
    category_id: Optional[str] = None,
    gender: Optional[str] = None,
    skip: int = 0,
    limit: int = 12,
    db: Session = Depends(database.get_db),
):
    query = db.query(models.Good)
    if category_id:
        query = query.filter(models.Good.category_id == category_id)
    if gender:
        query = query.filter(models.Good.gender == gender)

    goods = query.offset(skip).limit(limit).all()

    # Трансформуємо кожен товар у формат, який очікує GoodOut
    return [format_good(g) for g in goods]


@router.get("/{id}", response_model=schemas.GoodOut)
def get_good_detail(id: str, db: Session = Depends(database.get_db)):
    good = db.query(models.Good).filter(models.Good.id == id).first()
    if not good:
        raise HTTPException(status_code=404, detail="Product not found")

    # Повертаємо трансформований об'єкт
    return format_good(good)
