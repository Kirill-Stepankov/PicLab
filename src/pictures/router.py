from fastapi import APIRouter, UploadFile, Depends
from typing import Annotated
from .tasks import process_photo
from motor.motor_asyncio import AsyncIOMotorClient
from src.database import get_db
from .upload_config import ORIGINAL_DIR, PROCESSED_DIR, UPLOAD_DIR
from .schemas import Picture
import aiofiles
from celery.result import AsyncResult
from .schemas import Picture
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
import base64
from fastapi.responses import HTMLResponse


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.post('/upload_photo', response_model=Picture)
async def upload_photo(file: UploadFile, db : Annotated[AsyncIOMotorClient, Depends(get_db)]):
    photo_bytes = await file.read()

    result = process_photo.delay(photo_bytes)
    task_id = result.id

    UPLOAD_DIR.mkdir(exist_ok=True)
    PROCESSED_DIR.mkdir(exist_ok=True)
    ORIGINAL_DIR.mkdir(exist_ok=True)
    original_photo_path = ORIGINAL_DIR / f"{task_id}_original.jpg"
    processed_photo_path = PROCESSED_DIR / f"{task_id}_processed.jpg"

    async with aiofiles.open(original_photo_path, mode='wb') as f:
        contents = await f.write(photo_bytes)

    pic = Picture(
        task_id=task_id,
        original_url=str(original_photo_path),
        processed_url=str(processed_photo_path)
    )
    result = await db.test_collection.insert_one(pic.model_dump())

    return pic

@router.get('/picture/{pic_id}')
async def get_photo(request: Request, pic_id: str, db : Annotated[AsyncIOMotorClient, Depends(get_db)]):
    document = await db.test_collection.find_one({'task_id': pic_id})

    async with aiofiles.open(document['processed_url'], mode='rb') as f:
        proc_contents = await f.read()

    async with aiofiles.open(document['original_url'], mode='rb') as f:
        orig_contents = await f.read()


    base64_encoded_proc = base64.b64encode(proc_contents).decode("utf-8")
    base64_encoded_orig = base64.b64encode(orig_contents).decode("utf-8")


    context = {
        'request': request,
        'original_image': base64_encoded_orig,
        'processed_image': base64_encoded_proc
    }
    return templates.TemplateResponse('onepic.html', context=context)

    