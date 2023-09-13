from pydantic import BaseModel


class Picture(BaseModel):
    task_id: str
    original_url: str
    processed_url: str
