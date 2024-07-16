from pydantic import BaseModel
from uuid import UUID
from datetime import datetime



class File(BaseModel):
    '''
    Datamodel with file data
    '''
    file_id: UUID
    download_id: UUID
    size: int
    hash: str
    mime_type: str
    upload_at: datetime
