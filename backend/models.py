from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base
import pytz # 한국 시간대로 설졍

# 한국 시간대
kst = pytz.timezone('Asia/Seoul')

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
    created = Column(DateTime, default=datetime.now(kst))
    updated = Column(DateTime, default=datetime.now(kst), onupdate=datetime.now(kst))

    sessions = relationship("Session", backref="user")

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
    createdAt = Column(DateTime, default=lambda: datetime.now(kst))

    
class Exercise(Base):
    __tablename__ = "exercise"

    id = Column(Integer, primary_key=True)
    count = Column(Integer)
    time = Column(Integer)
    name = Column(String(20))
    set = Column(Integer)
    coordinate_list = Column(JSON)  # 좌표 리스트 
    
    sessions = relationship("Session", backref="exercise")


class Session(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    exercise_id = Column(Integer, ForeignKey("exercise.id"))
    date = Column(DateTime)

