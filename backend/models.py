from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(30))
    nickname = Column(String(20))
    password = Column(String(255))
    birth = Column(DateTime)
    gender = Column(Enum("Male", "Female"))
    height = Column(Integer, default=0)
    weight = Column(Integer, default=0)
    created = Column(DateTime, default=datetime.now(timezone.utc))
    updated = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

class Health(Base):
    __tablename__ = "health"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    waist = Column(Integer, default=0)
    leg = Column(Integer, default=0)
    pelvis = Column(Integer, default=0)
    neck = Column(Integer, default=0)
    need = Column(Integer, default=0)
    side_url = Column(String(500), index=True, default="url")
    front_url = Column(String(500), index=True, default="url")
    createdAt = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


