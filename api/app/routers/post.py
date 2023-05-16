from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import engine, get_db

router = APIRouter()

# Decorator for FastAPI
@router.get("/")
def root():
    return {"message": "Hello World"}

# Create 
@router.post("/user", status_code = status.HTTP_201_CREATED)
def create_posts(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_post = models.User(**user.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get user
@router.get("/user")
def get_user(db: Session = Depends(get_db)):
    posts = db.query(models.User).all()
    return posts

# Get post by id
@router.get("/user/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    posts = db.query(models.User).filter(models.User.id == id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return posts

# Delete by id
@router.delete("/user/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    posts = db.query(models.User).filter(models.User.id == id)
    if posts.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    posts.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update by id
@router.put("/user/{id}")
def update_post(id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    posts_query = db.query(models.User).filter(models.User.id == id)
    posts = posts_query.first()
    if posts == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND) 
    posts_query.update(user.dict(), synchronize_session=False)
    return{"data": posts_query.first()}

# @router.post("/exercise", status_code = status.HTTP_201_CREATED)
# def create_posts(post: schemas.exercise):
#     post_dict = post.dict()
#     exercise.append(post_dict)
#     return {"data": post_dict}

# @router.post("/score", status_code = status.HTTP_201_CREATED)
# def create_posts(post: score):
#     post_dict = post.dict()
#     score.append(post_dict)
#     return {"data": post_dict}