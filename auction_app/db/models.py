from sqlalchemy import Integer, String, Enum, ForeignKey, Text, DECIMAL, DateTime 
from auction_app.db.database import Base 
from typing import Optional, List  
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum
from datetime import datetime, date
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy import func


class RoleChoices(str, PyEnum):
    seller = 'seller'
    buyer = 'buyer'


class FuelType(str, PyEnum):
    hybrid = 'Гибрид'
    electric = 'Электр'
    gas = 'Газ'
    diesel = 'Дизель'
    petrol = 'Бензин'


class Transmission(str, PyEnum):
    mechanics = 'механика'
    auto = 'автомат'


class StatusCar(str, PyEnum):
    active = 'active'
    completed = 'completed'
    canceled = 'canceled'



class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices), nullable=False, default=RoleChoices.buyer)
    date_registered: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    seller_profile: Mapped[List['Car']] = relationship('Car', back_populates='seller',
                                                       cascade='all, delete-orphan')
    tokens: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user',
                                                        cascade='all, delete-orphan')
    bayer_profile: Mapped[List['Bid']] = relationship('Bid', back_populates='user',
                                                      cascade='all, delete-orphan')
    feedback: Mapped[List['Feedback']] = relationship(
        'Feedback',
        back_populates='seller_feedback',
        cascade='all, delete-orphan',
        foreign_keys='Feedback.seller_feedback_id'
    )

    bayer: Mapped[List['Feedback']] = relationship(
        'Feedback',
        back_populates='bayer',
        cascade='all, delete-orphan',
        foreign_keys='Feedback.bayer_id'
    )

    def set_passwords(self, password: str):
        self.hashed_password = bcrypt.hash(password)

    def check_password(self, password: str):
        return bcrypt.verify(password, self.hashed_password)

    def __str__(self):
        return f'{self.username}'


class RefreshToken(Base):
    __tablename__ = 'refresh_token'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_data: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='tokens')


class Car(Base):
    __tablename__ = 'car'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    brand: Mapped[str] = mapped_column(String(40))
    model: Mapped[str] = mapped_column(String(40))
    year: Mapped[date] = mapped_column(DateTime)
    fuel_type: Mapped[FuelType] = mapped_column(Enum(FuelType))
    transmission: Mapped[Transmission] = mapped_column(Enum(Transmission))
    mileage: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    description: Mapped[str] = mapped_column(Text)
    image: Mapped[str] = mapped_column(String)
    seller_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    seller: Mapped['UserProfile'] = relationship(UserProfile, back_populates='seller_profile')

    car_auction: Mapped['Auction'] = relationship('Auction', back_populates='car',
                                                  cascade='all, delete-orphan', uselist=False)


class Auction(Base):
    __tablename__ = 'auction'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    car_id: Mapped[int] = mapped_column(ForeignKey('car.id'), unique=True)
    car: Mapped['Car'] = relationship('Car', back_populates='car_auction')
    start_price: Mapped[int] = mapped_column(Integer, default=0)
    min_price: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[StatusCar] = mapped_column(Enum(StatusCar), default=StatusCar.active)

    bid_auction: Mapped['Bid'] = relationship("Bid", back_populates='auction',
                                              cascade='all, delete-orphan')


class Bid(Base):
    __tablename__ = 'bid'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    auction_id: Mapped[int] = mapped_column(ForeignKey('auction.id'))
    auction: Mapped['Auction']= relationship("Auction", back_populates='bid_auction')
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped['UserProfile'] = relationship(UserProfile, back_populates='bayer_profile')
    amount: Mapped[int] = mapped_column(Integer)
    date_registered: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Feedback(Base):
    __tablename__ = 'feedback'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    seller_feedback_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    seller_feedback: Mapped['UserProfile'] = relationship(UserProfile, back_populates='feedback',
                                                          foreign_keys=[seller_feedback_id]
    )
    bayer_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    bayer: Mapped['UserProfile'] = relationship(UserProfile, back_populates='bayer',
                                                foreign_keys=[bayer_id]
    )
    rating: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    create_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

