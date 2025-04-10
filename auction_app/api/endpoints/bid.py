from typing import List
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from auction_app.db.database import SessionLocal
from auction_app.db.models import Bid
from auction_app.db.schema import BidSchema

bid_router = APIRouter(prefix='/bid', tags=['Bid'])

# Dependency to get the DB session
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new bid
@bid_router.post('/', response_model=BidSchema, summary='Создать ставку')
async def create_bid(bid: BidSchema, db: Session = Depends(get_db)):
    bid_db = Bid(
        auction_id=bid.auction_id,
        user_id=bid.user_id,
        amount=bid.amount,
        date_registered=bid.date_registered
    )
    db.add(bid_db)
    db.commit()
    db.refresh(bid_db)
    return bid_db

# Get all bids for an auction
@bid_router.get('/auction/{auction_id}', response_model=List[BidSchema], summary='Получить все ставки для аукциона')
async def bid_list(auction_id: int, db: Session = Depends(get_db)):
    return db.query(Bid).filter(Bid.auction_id == auction_id).all()

# Get a bid by ID
@bid_router.get('/{bid_id}', response_model=BidSchema, summary='Получить ставку по ID')
async def bid_detail(bid_id: int, db: Session = Depends(get_db)):
    bid = db.query(Bid).filter(Bid.id == bid_id).first()

    if bid is None:
        raise HTTPException(status_code=404, detail='Ставка не найдена')
    return bid

# Delete a bid
@bid_router.delete('/{bid_id}', summary='Удалить ставку')
async def bid_delete(bid_id: int, db: Session = Depends(get_db)):
    bid_db = db.query(Bid).filter(Bid.id == bid_id).first()

    if bid_db is None:
        raise HTTPException(status_code=404, detail='Ставка не найдена')

    db.delete(bid_db)
    db.commit()
    return {'message': 'Ставка удалена'}
