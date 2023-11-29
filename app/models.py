from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class UserCard(Base):
    __tablename__ = "user_card"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    card_id = Column(Integer, ForeignKey("cards.id", ondelete='CASCADE'), nullable=False)

    cards = relationship("Card", back_populates="user_cards", cascade='all,delete')
    users = relationship("User", back_populates="user_cards", cascade='all,delete')


user_card = UserCard.__table__


class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    resourceURI = Column(String, nullable=False)

    users = relationship("User", secondary=UserCard, back_populates="card")


cards = Card.__table__


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    cards = relationship("Card", secondary=UserCard, back_populates="owners")


users = User.__table__
