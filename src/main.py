from fastapi import FastAPI
from .database import connect_and_init_db, close_db_connect, get_db
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from .pictures.router import router as pictures_router


app = FastAPI(
    title='Picture Lab'
)


app.add_event_handler("startup", connect_and_init_db)
app.add_event_handler("shutdown", close_db_connect)

app.include_router(
    pictures_router,
    tags=['Pictures']
)

