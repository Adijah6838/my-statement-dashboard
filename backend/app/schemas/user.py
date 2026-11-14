from pydantic import BaseModel, EmailStr
from typing import Optional

# Base schema with shared attributes
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

# Schema for registering a new user (includes password)
class UserCreate(UserBase):
    password: str

# Schema for returning user data (no passwords!)
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True