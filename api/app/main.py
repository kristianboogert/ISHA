from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from sqlalchemy.orm import Session
from pydantic import BaseModel
from random import randrange
from mysql.connector import Error
import mysql.connector
import time
from . import models, schemas
from .database import engine, get_db
from .routers import post


# models.Base.metadata.create_all(bind=engine)

# uvicorn api.app.main:app --reload
app = FastAPI()

# def create_db_connection(host_name, user_name, user_password, db_name): 
    # connection = None 
while True:
    try:
        connection = mysql.connector.connect(host = 'localhost', database = 'testdatabase', user = 'root', password = '')
        cursor = connection.cursor()
        # connection = mysql.connector.connect(
        #     host=host_name,
        #     user=user_name,
        #     passwd=user_password,
        #     database=db_name
        # )
        
        print("MySQL Database connection successful")
        break
    except Error as err:
        print(f"Error: '{err}'")
        time.sleep(2)

# mysql_connection = create_db_connection("127.0.0.1", "root", "", "testdatabase")

app.include_router(post.router)









# create database
@app.get("/sqlalchemy")
def test_user(db: Session = Depends(get_db)):
    return {"status": "succes"}


