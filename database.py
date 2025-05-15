from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship, sessionmaker, DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional, List
import datetime

# Инициализация базы данных
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[Optional[str]]
    full_name: Mapped[str]
    class_name: Mapped[str]
    registration_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    reviews: Mapped[List["Review"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, user_id={self.user_id!r}, class_name={self.class_name!r})"

class Review(Base):
    __tablename__ = "reviews"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    text: Mapped[str]
    rating: Mapped[int]  # От 1 до 5
    photo_id: Mapped[Optional[str]]
    date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    user: Mapped["User"] = relationship(back_populates="reviews")
    
    def __repr__(self) -> str:
        return f"Review(id={self.id!r}, rating={self.rating!r})"

# Создание движка и таблиц
engine = create_engine("sqlite:///school_canteen.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_session():
    """Возвращает новую сессию базы данных"""
    return Session() 