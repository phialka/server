from pydantic import BaseModel
from datetime import date
from typing import Optional


class UserCreate(BaseModel):
    name: str
    description: Optional[str] = None
    birthdate: Optional[date] = None
    tag: Optional[str] = None
    login: str
    password: str