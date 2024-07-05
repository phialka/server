from pydantic import BaseModel
from datetime import date
from typing import Optional


class MessageUpdate(BaseModel):
    content: Optional[str] = None

