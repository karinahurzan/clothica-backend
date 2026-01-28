from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID


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
    feedbacks_count: int
    feedbacks_average: float


class GoodOut(GoodBase):
    id: str

    class Config:
        from_attributes = True


class GoodsPagination(BaseModel):
    items: List[GoodOut]
    total_count: int
    has_more: bool
    max_available_price: int


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
    id: UUID
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
    id: UUID
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
    id: UUID
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class SubscriptionCreate(BaseModel):
    email: EmailStr


class TokenRefreshRequest(BaseModel):
    refresh_token: str
