from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


class Price(BaseModel):
    value: float
    currency: str


class CategoryBase(BaseModel):
    name: str


class CategoryOut(CategoryBase):
    id: str

    class Config:
        from_attributes = True


class GoodBase(BaseModel):
    name: str
    category_id: str
    image: str
    price: Price
    size: List[str]
    description: str
    prevDescription: str
    gender: str
    characteristics: List[str]


class GoodOut(GoodBase):
    id: str

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserOut(UserBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    token: str


class FeedbackBase(BaseModel):
    author: str
    description: str
    rate: float
    product_id: str


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackOut(FeedbackBase):
    id: int
    date: datetime

    class Config:
        from_attributes = True


class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: float


class OrderCreate(BaseModel):
    items: List[OrderItem]
    total_price: float
    user_id: Optional[int] = None


class OrderOut(OrderCreate):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class SubscriptionCreate(BaseModel):
    email: EmailStr
