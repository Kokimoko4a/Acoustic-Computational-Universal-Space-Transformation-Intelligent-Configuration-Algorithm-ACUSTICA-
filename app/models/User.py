from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class User(BaseModel):
    # [Key] - Optional, защото в началото нямаме ID (преди записа в БД)
    id: Optional[int] = None

    # [Required], [StringLength(100, MinimumLength=3)]
    username: str = Field(..., min_length=3, max_length=100)

    # [Required], [EmailAddress]
    email: EmailStr

    # [Required], [StringLength(100)]
    first_name: str = Field(..., max_length=100)

    # [Required], [StringLength(100)]
    last_name: str = Field(..., max_length=100)

    # [Required], [Range(1, 120)]
    age: Optional[int] = None

    hashed_password: str = Field(..., max_length= 256)

    

    # Пример за изчислено свойство (като Read-only Property в C#)
    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
