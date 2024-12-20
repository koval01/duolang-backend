import enum
from sqlalchemy import Column, String, BigInteger, Enum, Boolean
from sqlalchemy.orm import relationship

from .base import PkBase


class RoleEnum(enum.Enum):
    user = 1
    admin = 2


class Profile(PkBase):
    __tablename__ = 'profile'

    displayName = Column(String(255), nullable=False)
    telegram = Column(BigInteger, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.user)
    visible = Column(Boolean, default=False)
    avatar = Column(String(2048))

    # Relationship with Lesson
    lessons = relationship('Lesson', back_populates='profile', cascade='all, delete-orphan')
