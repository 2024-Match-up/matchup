from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(20))
    nickname = Column(String(20))
    password = Column(String(20))

    records = relationship("Record", backref="user")
    healths = relationship("Health", backref="user")

class Exercise(Base):
    __tablename__ = "exercise"

    id = Column(Integer, primary_key=True)
    count = Column(Integer)
    time = Column(Integer)
    name = Column(String(20))

    records = relationship("Record", backref="exercise")

class Record(Base):
    __tablename__ = "record"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    exercise_id = Column(Integer, ForeignKey("exercise.id"))
    date = Column(DateTime)
    week = Column(Integer)
    set = Column(Integer)

class HealthRecord(Base):
    __tablename__ = "health"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    bmi = Column(Integer)
    height = Column(Integer)
    weight = Column(Integer)
    waist = Column(Integer)
    leg = Column(Integer)
    pelvis = Column(Integer)
    neck = Column(Integer)
    gender = Column(Enum("Male", "Female"))
    birth = Column(DateTime)
