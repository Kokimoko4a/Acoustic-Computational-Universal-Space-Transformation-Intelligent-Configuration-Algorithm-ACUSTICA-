from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from models.Audio import Audio
from models.User import User

class Scene(BaseModel):

    id: Optional[int] = None 

    audio_file: Audio

    scene_label: str = Field(..., max_length= 200)

    room_settings: dict

    user: User
