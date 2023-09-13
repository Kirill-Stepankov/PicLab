from fastapi import FastAPI
from .database import connect_and_init_db, close_db_connect, get_db
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI(
    title='Picture Lab'
)

app.add_event_handler("startup", connect_and_init_db)
app.add_event_handler("shutdown", close_db_connect)


@app.get('/')
async def health(db: AsyncIOMotorClient = Depends(get_db)):
    try:
        # Check if the database is responsive
        await db.command('ping')
        db_status = 'up'
    except Exception:
        db_status = 'down'

    return {
        "database": db_status
    }