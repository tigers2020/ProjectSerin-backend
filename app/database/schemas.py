from typing import Dict, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserUpdate(UserBase):
    name: str | None = None
    persona: Dict[str, str] | None = None
    avatar_url: Optional[str] = None  # Add this line


class UserCreate(UserBase):
    password: str
    avatar_url: Optional[str] = None  # Add this line
    persona: Optional[Dict[str, str]] = None  # Add this line


class User(BaseModel):
    id: int
    name: str
    email: str
    persona: Dict[str, str]
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class UserLogin(BaseModel):
    email: str
    password: str
