from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    id:         int
    name:       str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class ExerciseBase(BaseModel):
    id:         int
    user_id:    int
    score_id:   int

class ExerciseCreate(ExerciseBase):
    pass

class ExerciseUpdate(ExerciseBase):
    pass

class ScoreBase(BaseModel):
    id:         int
    exercise_id:int 
    user_id:    int
    value:      str   

class ScoreCreate(ScoreBase):
    pass

class ScoreUpdate(ScoreBase):
    pass

