from fastapi import Depends, FastAPI, Response, status,HTTPException
from pydantic import BaseModel
from . import models, schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List


app= FastAPI()

from . import schemas, models

# used to migrate models to database in table

models.Base.metadata.create_all(engine)

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog')
def create(request:schemas.Blog, db:Session= Depends(get_db)):
    new_blog= models.Blog(title=request.title, body= request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog',response_model=List[schemas.ShowBlog])
def all(db:Session= Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs



@app.get('/blog/{id}', status_code=200,response_model=schemas.ShowBlog)
def show(id,response:Response ,db:Session= Depends(get_db)):
    blog= db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        response.status_code=status.HTTP_404_NOT_FOUND
    return blog


@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request: schemas.Blog, db:Session= Depends(get_db)):
    
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    else:
        blog.update(request)
        db.commit()
        return 'updated'
    
    
@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,db:Session= Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    else:
        blog.delete(synchronize_session=False)
        db.commit()
        return 'deleted'
    
    
    
@app.post('/user')
def create_user(request: schemas.User,db:Session= Depends(get_db)):
    
    new_user=models.User(name=request.name, email=request.email, password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/users',)
def all(db:Session= Depends(get_db)):
    users=db.query(models.User).all()
    return users

@app.delete('/user/{id}')
def user_delete(id,db:Session= Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found")
    user.delete(synchronize_session=False)
    db.commit()
    return 'deleted'
    
    







