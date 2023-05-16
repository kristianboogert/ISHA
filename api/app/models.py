from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)

class Exercise(Base):
    __tablename__ = "exercise"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, nullable=False)

class Score(Base):
    __tablename__ = "score"
    id = Column(Integer, primary_key=True, nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercise.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    value = Column(String, nullable=False)

class Metadata(Base):
    __tablename__ = "metadata"
    id = Column(Integer, primary_key=True, nullable=False)
    bodypart_name = Column(String, nullable=False)
    bodypart_angle_xy = Column(Integer, nullable=False)
    bodypart_angle_yz = Column(Integer, nullable=False)
    bodypart_angle_xz = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    score_id = Column(Integer, ForeignKey("score.id"), nullable=False)