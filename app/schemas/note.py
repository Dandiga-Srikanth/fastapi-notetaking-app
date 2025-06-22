from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.user import UserRead
from pydantic.alias_generators import to_camel

class NoteBase(BaseModel):
    title: str = Field(..., max_length=255)
    content: str = Field(..., min_length=1, max_length=5000)

    class Config:
        from_attributes = True
        alias_generator = to_camel
        validate_by_name = True

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = None

class NoteRead(NoteBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    owner: Optional[UserRead] = None