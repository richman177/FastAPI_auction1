from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from auction_app.db.models import RoleChoices, FuelType, Transmission, StatusCar


class UserProfileSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    hashed_password: str
    phone_number: Optional[str]
    role: RoleChoices
    date_registered: datetime


class CarSchema(BaseModel):
    id: int
    brand: str
    model: str
    year: date
    fuel_type: FuelType
    transmission: Transmission
    mileage: int
    price: float
    description: str
    image: str
    seller_id: int


class AuctionSchema(BaseModel):
    id: int
    car_id: int
    start_price: int
    min_price: Optional[int]
    start_time: datetime
    end_time: datetime
    status: StatusCar


class BidSchema(BaseModel):
    id: int
    auction_id: int
    user_id: int
    amount: int
    date_registered: datetime


class FeedbackSchema(BaseModel):
    id: int
    seller_feedback_id: int
    bayer_id: int
    rating: int
    text: str
    create_date: datetime
