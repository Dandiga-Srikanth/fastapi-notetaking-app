from pydantic import BaseModel

class RoleBase(BaseModel):
    name: str

    class Config:
        from_attributes = True

class RoleRead(RoleBase):
    id: int
