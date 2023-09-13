from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import logging
from pathlib import Path
import os

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

db_client: AsyncIOMotorClient = None


async def get_db() -> AsyncIOMotorClient:
    db_name = os.getenv('MONGO_DB_NAME')
    return db_client[db_name]


async def connect_and_init_db():
    global db_client
    try:
        db_client = AsyncIOMotorClient(
            os.getenv('MONGO_DB_HOST'),
            username=os.getenv('MONGO_DB_USERNAME'),
            password=os.getenv('MONGO_DB_PASSWORD'),
            uuidRepresentation="standard",
        )
        logging.info('Connected to mongo.')
    except Exception as e:
        logging.exception(f'Could not connect to mongo: {e}')
        raise


async def close_db_connect():
    global db_client
    if db_client is None:
        logging.warning('Connection is None, nothing to close.')
        return
    db_client.close()
    db_client = None
    logging.info('Mongo connection closed.')