from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    email: str = Field(...)
    password: str = Field(..., min_length=5)

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id:Optional[int]