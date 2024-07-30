from datetime import datetime
from uuid import UUID
from typing import Optional, Literal

from pydantic import BaseModel


class ProfileItemUpdate(BaseModel):
    displayName: Optional[str] = None
    description: Optional[str] = None
    visible: Optional[bool] = False


class ProfileItem(ProfileItemUpdate):
    id: UUID
    createdAt: datetime
    telegram: Optional[int] = None
    role: Optional[Literal["user", "admin"]] = "user"
    avatar: Optional[str] = None


class ProfileItemDisplay(ProfileItemUpdate):
    id: UUID
    createdAt: datetime
    telegram: Optional[int] = None
    avatar: Optional[str] = None


class ProfileItemCreate(BaseModel):
    telegram: int
    displayName: str


class ProfileItemInit(BaseModel):
    id: UUID
