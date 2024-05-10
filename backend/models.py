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

    healths = relationship("Health", backref="user")
    # sessions = relationship("Session", backref="user")
    # exercises = relationship("Exercise", backref="user")

# class Exercise(Base):
#     __tablename__ = "exercise"

#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("user.id"))
#     count = Column(Integer)
#     time = Column(Integer)
#     name = Column(String(20))
#     set = Column(Integer)
#     rep = Column(Integer)

#     records = relationship("Session", backref="exercise")

# class Session(Base):
#     __tablename__ = "session"

#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("user.id"))
#     exercise_id = Column(Integer, ForeignKey("exercise.id"))
#     date = Column(DateTime)
#     week = Column(Integer)
#     set = Column(Integer)

class Health(Base):
    __tablename__ = "health"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    waist = Column(Integer)
    leg = Column(Integer)
    pelvis = Column(Integer)
    neck = Column(Integer)
    date_added = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    need = Column(Integer)
