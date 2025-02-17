from pydantic import BaseModel, EmailStr
from typing import Optional

# Base schema (shared fields)
class UserBase(BaseModel):
    username: str
    email: EmailStr
    phone_number: Optional[str] = None
    is_admin: bool = False

# User creation (includes password)
class UserCreate(UserBase):
    password: str

# Response schema (excludes password)
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True  # Converts SQLAlchemy object to Pydantic
