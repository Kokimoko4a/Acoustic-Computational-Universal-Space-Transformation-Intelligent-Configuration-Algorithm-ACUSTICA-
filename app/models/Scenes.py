from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from Audio import Audio
from User import User

class Scene(BaseModel):

    id: Optional[int] = None 

    audio_file: Audio

    scene_label: str = Field(..., max_length= 200)

    room_settings: dict 

    user: User
