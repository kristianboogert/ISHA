from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    id:             int
    name:           str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserDelete(UserBase):
    pass

class ExerciseBase(BaseModel):
    id:             int
    name:           str
    type:           str
    description:    str

class ExerciseCreate(ExerciseBase):
    pass

class ExerciseUpdate(ExerciseBase):
    pass

class ExerciseDelete(ExerciseBase):
    pass

class ScoreBase(BaseModel):
    id:             int
    exercise_id:    int 
    user_id:        int
    value:          str   

class ScoreCreate(ScoreBase):
    pass

class ScoreUpdate(ScoreBase):
    pass

class ScoreDelete(ScoreBase):
    pass

class MetadataBase(BaseModel):
    id:                 int
    bodypart_name:      str
    bodypart_angle_xy:  str
    bodypart_angle_yz:  str
    bodypart_angle_xz:  str
    created_at:         datetime
    score_id:           int

class MetadataCreate(MetadataBase):
    pass

class MetadataUpdate(MetadataBase):
    pass

class MetadataDelete(MetadataBase):
    pass