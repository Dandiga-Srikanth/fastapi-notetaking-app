from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.schemas.role import RoleRead
from app.core.config import RoleEnum

class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)

    class Config:
        from_attributes = True
        alias_generator = lambda s: ''.join([s[0].lower()] + [c if c.islower() else f"{c}" for c in s[1:]])
        validate_by_name = True
        use_enum_values = False

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    role_name: RoleEnum = RoleEnum.viewer

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)


class UserRead(UserBase):
    id: int
    role: Optional[RoleRead] = None