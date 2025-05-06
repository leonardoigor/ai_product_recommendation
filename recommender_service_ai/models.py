from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
import os

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    interactions = relationship("UserInteraction", back_populates="user")
    scores = relationship("UserItemScore", back_populates="user")


class Item(Base):
    __tablename__ = "items"
    item_id = Column(Integer, primary_key=True)
    category = Column(String(50))
    interactions = relationship("UserInteraction", back_populates="item")
    scores = relationship("UserItemScore", back_populates="item")


class UserInteraction(Base):
    __tablename__ = "user_interactions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    item_id = Column(Integer, ForeignKey("items.item_id"))
    interaction_type = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="interactions")
    item = relationship("Item", back_populates="interactions")


class UserItemScore(Base):
    __tablename__ = "user_item_scores"
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    item_id = Column(Integer, ForeignKey("items.item_id"), primary_key=True)
    relevance_score = Column(Float)
    last_updated = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="scores")
    item = relationship("Item", back_populates="scores")


# Configuração da conexão
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
