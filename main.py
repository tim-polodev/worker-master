from dotenv import load_dotenv
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

load_dotenv()
from contextlib import asynccontextmanager

from fastapi import FastAPI

from config.database import db_mongo
from config.ratelimiter import limiter
from routes import tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_mongo.connect()
    yield
    db_mongo.close()


app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(tasks_router, tags=["Tasks"], prefix="/api/v1")
