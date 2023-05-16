from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    id:         int
    name:       str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class exercise(BaseModel):
    id:         int
    user_id:    int
    score_id:   int

class score(BaseModel):
    id:         int
    exercise_id:int 
    user_id:    int
    value:      str   