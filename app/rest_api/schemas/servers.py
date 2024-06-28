from pydantic import BaseModel
from datetime import date
from typing import Optional



class ServerCreate(BaseModel):
    title: str
    description: Optional[str] = None



class ServerUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


