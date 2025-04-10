from fastapi import FastAPI
from sqladmin import Admin
from auction_app.admin.view import UserProfileAdmin, CarAdmin, AuctionAdmin, BidAdmin, FeedbackAdmin
from auction_app.db.database import engine


def setup_admin(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(CarAdmin)
    admin.add_view(AuctionAdmin)
    admin.add_view(BidAdmin)
    admin.add_view(FeedbackAdmin)


