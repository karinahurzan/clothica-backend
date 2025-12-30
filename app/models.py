from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    ForeignKey,
    JSON,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression
from .database import Base
import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_admin = Column(Boolean, default=False)
    orders = relationship("Order", back_populates="owner")


class Good(Base):
    __tablename__ = "goods"

    id = Column(
        String,
        primary_key=True,
        nullable=False,
    )
    name = Column(String, nullable=False)
    category_id = Column(String, ForeignKey("categories.id"))
    image = Column(String)
    price_value = Column(Float)
    price_currency = Column(String)
    size = Column(JSON)
    description = Column(String)
    prevDescription = Column(String)
    gender = Column(String)
    characteristics = Column(JSON)


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(
        String,
        primary_key=True,
        nullable=False,
    )
    author = Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    description = Column(String)
    rate = Column(Float)
    product_id = Column(String, ForeignKey("goods.id"))


class Category(Base):
    __tablename__ = "categories"
    id = Column(String, primary_key=True)
    name = Column(String)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    items = Column(JSON)
    total_price = Column(Float)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    owner = relationship("User", back_populates="orders")


class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
