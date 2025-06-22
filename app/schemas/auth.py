from pydantic import BaseModel
from typing import Optional


class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class DataToken(BaseModel):
    user_id: Optional[int] = None