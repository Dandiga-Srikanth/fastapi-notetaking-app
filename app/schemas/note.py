from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class NoteBase(BaseModel):
    title: str = Field(..., max_length=255)
    content: str = Field(..., min_length=1, max_length=5000)

    class Config:
        orm_mode = True
        alias_generator = lambda s: ''.join([s[0].lower()] + [c if c.islower() else f"{c}" for c in s[1:]])
        allow_population_by_field_name = True

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = None

class NoteRead(NoteBase):
    id: int
    owner_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
