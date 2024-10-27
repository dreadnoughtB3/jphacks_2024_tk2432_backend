from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone
import uuid

class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, index=True, nullable=False, unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True, index=True)
    hashed_password: str = Field(nullable=False)
    nick_name: str = Field(nullable=False)

    letters: List["Letters"] = Relationship(back_populates="user")

class Letters(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.uid", nullable=False, index=True)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    happy: bool = Field(default=False, nullable=False)
    healing: bool = Field(default=False, nullable=False)
    amusing: bool = Field(default=False, nullable=False)
    negative: bool = Field(default=False, nullable=False)

    user: Optional[Users] = Relationship(back_populates="letters")
