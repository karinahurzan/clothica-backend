from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, database

router = APIRouter()


def format_good(good):
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


@router.get("/", response_model=schemas.GoodsPagination)
def get_goods(
    category_id: Optional[str] = None,
    gender: Optional[str] = None,
    size: Optional[List[str]] = Query(None),
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    skip: int = 0,
    limit: int = 12,
    db: Session = Depends(database.get_db),
):
    query = db.query(models.Good)

    if category_id:
        query = query.filter(models.Good.category_id == category_id)
    if gender:
        query = query.filter(models.Good.gender == gender)
    if size:
        query = query.filter(models.Good.size.contains(size))

    max_price_in_db = (
        query.with_entities(func.max(models.Good.price_value)).scalar() or 1000
    )

    print(max_price_in_db)

    if min_price is not None:
        query = query.filter(models.Good.price_value >= min_price)
    if max_price is not None:
        query = query.filter(models.Good.price_value <= max_price)

    total_count = query.count()
    goods = query.offset(skip).limit(limit).all()

    return {
        "items": [format_good(g) for g in goods],
        "total_count": total_count,
        "has_more": skip + limit < total_count,
        "max_available_price": max_price_in_db,
    }


@router.get("/{id}", response_model=schemas.GoodOut)
def get_good_detail(id: str, db: Session = Depends(database.get_db)):
    good = db.query(models.Good).filter(models.Good.id == id).first()
    if not good:
        raise HTTPException(status_code=404, detail="Product not found")

    return format_good(good)
