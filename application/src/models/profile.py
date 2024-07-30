import enum
from sqlalchemy import Column, String, BigInteger, Enum, Boolean

from ..models.base import PkBase


class RoleEnum(enum.Enum):
    user = 1
    admin = 2


class Profile(PkBase):
    """Profile model"""
    __tablename__ = 'profile'

    displayName = Column(String(255), nullable=False)
    telegram = Column(BigInteger, nullable=False)
    role = Column(Enum(RoleEnum), default="user")
    visible = Column(Boolean, default=False)
    avatar = Column(String(2048))
