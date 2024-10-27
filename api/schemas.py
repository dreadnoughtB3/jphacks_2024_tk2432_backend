# app/schemas.py
from pydantic import BaseModel
import uuid
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: str
    hashed_password: str
    nick_name: str
    description: str

class UserRead(BaseModel):
    id: int
    uid: uuid.UUID
    name: str
    nick_name: str
    email: str
    hashed_password: str
    description: str
    created_at: datetime
    updated_at: datetime

class LetterCreate(BaseModel):
    content: str
    user_id: str
    happy: int
    healing: int
    negative: int
    amusing: int