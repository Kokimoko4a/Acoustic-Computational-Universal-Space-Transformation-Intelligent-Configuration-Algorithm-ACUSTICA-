from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from User import User

class Audio(BaseModel):

    id: Optional[int] = None

    user: User

    file_name: str = Field(..., max_length= 255)

    file_path: str

    created_at: datetime = Field(default_factory=datetime.now)