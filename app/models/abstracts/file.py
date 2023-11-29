from abc import ABCMeta, abstractmethod
from typing import Optional, Union

from pydantic import BaseModel



class AbsFile(BaseModel):
    __metaclass__ = ABCMeta

    class PhotoTI(BaseModel):
        width: int
        height: int

    class VideoTI(BaseModel):
        width: int
        height: int
        duration: int

    class AudioTI(BaseModel):
        duration: int
    

    id: int
    hash: str
    size: int
    type: str
    location: str
    title: str
    type_info: Union[PhotoTI, VideoTI, AudioTI, None]