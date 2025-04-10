import fastapi
import uvicorn
from fastapi import FastAPI
import redis.asyncio as redis
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter
from auction_app.admin.setup import setup_admin
from auction_app.db.database import SessionLocal
from auction_app.api.endpoints import auth, car, auction, bid, feedback
from starlette.middleware.sessions import SessionMiddleware
from fastapi_pagination import add_pagination


async def init_redis():
    return redis.Redis.from_url("redis://localhost", encoding='utf-8', decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await init_redis()
    await FastAPILimiter.init(redis)
    yield
    await redis.aclose()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

auction_app = fastapi.FastAPI(title='Auction site', lifespan=lifespan)
auction_app.add_middleware(SessionMiddleware, secret_key='SECRET_KEY')

setup_admin(auction_app)
add_pagination(auction_app)

auction_app.include_router(auth.auth_router)
auction_app.include_router(car.car_router)
auction_app.include_router(auction.auction_router)
auction_app.include_router(bid.bid_router)
auction_app.include_router(feedback.feedback_router)


if __name__ == "__main__":
    uvicorn.run(auction_app, host="127.0.0.1", port=8001)