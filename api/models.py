from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, index=True, nullable=False, unique=True)
    created_at: datetime = Field(default=datetime.now, nullable=False)
    updated_at: datetime = Field(default=datetime.now, nullable=False)
    name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True, index=True)
    hashed_password: str = Field(nullable=False)
    nick_name: str = Field(nullable=False)

    letters: List["Letters"] = Relationship(back_populates="user")

class Letters(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.uid", nullable=False, index=True)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now, nullable=False)
    happy: int = Field(default=0, nullable=False)
    healing: int = Field(default=0, nullable=False)
    amusing: int = Field(default=0, nullable=False)
    negative: int = Field(default=0, nullable=False)

    user: Optional[Users] = Relationship(back_populates="letters")
