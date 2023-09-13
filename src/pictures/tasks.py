from .celery import app_celery
import cv2
from io import BytesIO
from PIL import Image
import json
from .upload_config import UPLOAD_DIR, PROCESSED_DIR, ORIGINAL_DIR


@app_celery.task
def process_photo(photo_bytes):
    image = Image.open(BytesIO(photo_bytes))

    bw_image = image.convert('L')

    output_buffer = BytesIO()
    bw_image.save(output_buffer, format='JPEG')
    processed_photo_bytes = output_buffer.getvalue()

    photo_id = process_photo.request.id

    UPLOAD_DIR.mkdir(exist_ok=True)
    PROCESSED_DIR.mkdir(exist_ok=True)
    ORIGINAL_DIR.mkdir(exist_ok=True)

    processed_photo_path = PROCESSED_DIR / f"{photo_id}_processed.jpg"

    with processed_photo_path.open("wb") as f:
            f.write(processed_photo_bytes)

    return 'OK'