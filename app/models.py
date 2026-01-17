import uuid
from sqlalchemy import (
    Column,
    String,
    Float,
    ForeignKey,
    JSON,
    Boolean,
    DateTime,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression
from .database import Base
import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_admin = Column(Boolean, default=False)
    orders = relationship("Order", back_populates="owner")


class Good(Base):
    __tablename__ = "goods"

    id = Column(String, primary_key=True, index=True)
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

    feedbacks = relationship("Feedback", back_populates="goods")


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    author = Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    description = Column(String)
    rate = Column(Float)
    product_id = Column(String, ForeignKey("goods.id"))

    goods = relationship("Good", back_populates="feedbacks")


class Category(Base):
    __tablename__ = "categories"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)


class Order(Base):
    __tablename__ = "orders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    items = Column(JSON)
    total_price = Column(Float)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    owner = relationship("User", back_populates="orders")


class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True)


class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"

    id = Column(String, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    blacklisted_on = Column(DateTime(timezone=True), server_default=func.now())
