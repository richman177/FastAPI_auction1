from sqladmin import ModelView
from auction_app.db.models import UserProfile, Car, Auction, Bid, Feedback


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.username]
    name = 'User'
    name_plural = 'Users'


class CarAdmin(ModelView, model=Car):
    column_list = [Car.id, Car.model] 
    name = 'Car'
    name_plural = 'Car'


class AuctionAdmin(ModelView, model=Auction):
    column_list = [Auction.id]
    name = 'Auction'
    name_plural = 'Auction'


class BidAdmin(ModelView, model=Bid): 
    column_list = [Bid.id, Bid.user]
    name = 'Bid'
    name_plural = 'Bid'


class FeedbackAdmin(ModelView, model=Feedback):
    column_list = [Feedback.id, Feedback.text]
    name = 'Feedback'
    name_plural = 'Feedback'
