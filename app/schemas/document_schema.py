
from pydantic import BaseModel
from datetime import datetime
import uuid

class DocumentResponse(BaseModel):
    id: str
    filename: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True