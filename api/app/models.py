from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, any_
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from random import randrange
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, default=None, primary_key=True, autoincrement="auto")
    name = Column(String(100), nullable=False)

class Exercise(Base):
    __tablename__ = "exercise"
    id = Column(Integer, default=None, primary_key=True, autoincrement="auto")
    name = Column(String(100), nullable=False)
    type = Column(String(100), nullable=False)
    description = Column(String(200), nullable=False)

class Score(Base):
    __tablename__ = "score"
    id = Column(Integer, default=None, primary_key=True, autoincrement="auto")
    exercise_id = Column(Integer, ForeignKey("exercise.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    value = Column(Integer, nullable=False)

class Metadata(Base):
    __tablename__ = "metadata"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement="auto")
    bodypart_name = Column(String(100), nullable=False)
    bodypart_angle_xy = Column(Integer, nullable=False)
    bodypart_angle_yz = Column(Integer, nullable=False)
    bodypart_angle_xz = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    score_id = Column(Integer, ForeignKey("score.id", ondelete="CASCADE"))