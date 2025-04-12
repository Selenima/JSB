from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, ForeignKey, func
from sqlalchemy.orm import relationship
from models.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    tg_user_id = Column(Integer, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    profile = relationship('Profile', back_populates="user", uselist=False)
    ticket = None

class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_user_id = Column(ForeignKey('users.tg_user_id'), nullable=False)
    fullname = Column(String, nullable=True)
    company = Column(String, nullable=True)
    position = Column(String, nullable=True)
    contacts = Column(JSON, server_default='[]', default=list)

    user = relationship('User', back_populates='profile', uselist=False)

