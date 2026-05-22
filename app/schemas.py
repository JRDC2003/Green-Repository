"""Pydantic schemas."""
from pydantic import BaseModel, EmailStr, Field
from typing import Any, Optional
from datetime import datetime


class UserRegister(BaseModel):
    """User registration request schema."""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=50)
    email: EmailStr
    phone: str = Field(..., max_length=12)


class UserLogin(BaseModel):
    """User login request schema."""
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=50)


class UserResponse(BaseModel):
    """User response schema."""
    id: int
    username: str
    email: str
    phone: str
    registered_date: datetime
    
    class Config:
        from_attributes = True
