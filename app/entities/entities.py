from typing import Union, Optional
from pydantic import BaseModel, ByteSize
from uuid import UUID, uuid4
from datetime import datetime



class File(BaseModel):
    file_id: UUID
    download_id: UUID
    size: ByteSize
    hash: str
    mime_type: str
    upload_at: datetime



class FileFilter(BaseModel):
    file_id: Optional[UUID] = None
    download_id: Optional[UUID] = None
    hash: Optional[str] = None
    min_upload_datetime: Optional[datetime] = None
    max_upload_datetime: Optional[datetime] = None
