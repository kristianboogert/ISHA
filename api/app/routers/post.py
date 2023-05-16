from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import engine, get_db

router = APIRouter()

# Decorator for FastAPI
@router.get("/")
def root():
    return {"message": "Hello World"}

# Get users
@router.get("/user")
def get_user(db: Session = Depends(get_db)):
    posts = db.query(models.User).all()
    return posts

# Create user
@router.post("/user", status_code = status.HTTP_201_CREATED)
def create_posts(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_post = models.User(**user.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get user by id
@router.get("/user/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    posts = db.query(models.User).filter(models.User.id == id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return posts

# Delete user by id
@router.delete("/user/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    posts = db.query(models.User).filter(models.User.id == id)
    if posts.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    posts.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update user by id
@router.put("/user/{id}")
def update_post(id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    posts_query = db.query(models.User).filter(models.User.id == id)
    posts = posts_query.first()
    if posts == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND) 
    posts_query.update(user.dict(), synchronize_session=False)
    return{"data": posts_query.first()}


# Create exercise
@router.post("/exercise", status_code = status.HTTP_201_CREATED)
def create_posts(exercise: schemas.ExerciseCreate, db: Session = Depends(get_db)):
    new_post = models.Exercise(**exercise.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get exercise by id
@router.get("/exercise/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    posts = db.query(models.Exercise).filter(models.Exercise.id == id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return posts

# Delete exercise by id
@router.delete("/exercise/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    posts = db.query(models.Exercise).filter(models.Exercise.id == id)
    if posts.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    posts.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update exercise by id
@router.put("/user/{id}")
def update_post(id: int, exercise: schemas.ExerciseUpdate, db: Session = Depends(get_db)):
    posts_query = db.query(models.Exercise).filter(models.Exercise.id == id)
    posts = posts_query.first()
    if posts == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND) 
    posts_query.update(exercise.dict(), synchronize_session=False)
    return{"data": posts_query.first()}


# Create score
@router.post("/score", status_code = status.HTTP_201_CREATED)
def create_posts(score: schemas.ScoreCreate, db: Session = Depends(get_db)):
    new_post = models.Score(**score.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get exercise by id
@router.get("/score/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    posts = db.query(models.Score).filter(models.Score.id == id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return posts

# Delete exercise by id
@router.delete("/score/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    posts = db.query(models.Score).filter(models.Score.id == id)
    if posts.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    posts.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update score by id
@router.put("/score/{id}")
def update_post(id: int, score: schemas.ScoreUpdate, db: Session = Depends(get_db)):
    posts_query = db.query(models.Score).filter(models.Score.id == id)
    posts = posts_query.first()
    if posts == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND) 
    posts_query.update(score.dict(), synchronize_session=False)
    return{"data": posts_query.first()}


# Create metadata
@router.post("/metadata", status_code = status.HTTP_201_CREATED)
def create_posts(metadata: schemas.MetadataCreate, db: Session = Depends(get_db)):
    new_post = models.Metadata(**metadata.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get metadata by id
@router.get("/metadata/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    posts = db.query(models.Metadata).filter(models.Metadata.id == id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return posts

# Delete metadata by id
@router.delete("/metadata/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    posts = db.query(models.Metadata).filter(models.Metadata.id == id)
    if posts.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    posts.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update metadata by id
@router.put("/metadata/{id}")
def update_post(id: int, metadata: schemas.MetadataUpdate, db: Session = Depends(get_db)):
    posts_query = db.query(models.Metadata).filter(models.Metadata.id == id)
    posts = posts_query.first()
    if posts == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND) 
    posts_query.update(metadata.dict(), synchronize_session=False)
    return{"data": posts_query.first()}