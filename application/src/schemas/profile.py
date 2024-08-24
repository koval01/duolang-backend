from datetime import datetime
from uuid import UUID
from typing import Literal

from pydantic import BaseModel


class ProfileItemUpdate(BaseModel):
    displayName: str | None = None
    visible: bool | None = None


class ProfileItem(ProfileItemUpdate):
    id: UUID
    createdAt: datetime
    role: Literal["user", "admin"] = "user"
    avatar: str | None = None


class ProfileItemDisplay(ProfileItemUpdate):
    id: UUID
    createdAt: datetime
    telegram: int | None = None
    avatar: str | None = None

    class Config:
        from_attributes = True


class ProfileItemCreate(BaseModel):
    telegram: int
    displayName: str


class ProfileItemInit(BaseModel):
    id: UUID
