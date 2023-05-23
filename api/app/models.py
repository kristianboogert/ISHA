from .database import Base
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, any_, func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from random import randrange
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlmodel import SQLModel, Field

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, default=None, primary_key=True, autoincrement="auto")
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    last_edited = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

class Exercise(Base):
    __tablename__ = "exercise"
    id = Column(Integer, default=None, primary_key=True, autoincrement="auto")
    name = Column(String(100), nullable=False)
    type = Column(String(100), nullable=False)
    description = Column(String(200), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    last_edited = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

class Score(Base):
    __tablename__ = "score"
    id = Column(Integer, default=None, primary_key=True, autoincrement="auto")
    exercise_id = Column(Integer, ForeignKey("exercise.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    value = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    last_edited = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

class Metadata(Base):
    __tablename__ = "metadata"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    bodypart_name = Column(String(100), nullable=False)
    bodypart_angle_xy = Column(Integer, nullable=False)
    bodypart_angle_yz = Column(Integer, nullable=False)
    bodypart_angle_xz = Column(Integer, nullable=False)
    score_id = Column(Integer, ForeignKey("score.id", ondelete="CASCADE"))
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    last_edited = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)