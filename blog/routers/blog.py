from fastapi import APIRouter, Depends,Response, status,HTTPException
from typing import List
from .. import schemas, models, database
from ..oauth2 import get_current_user
from sqlalchemy.orm import Session

from ..database import get_db

router= APIRouter(
     tags=['Blogs']
)




@router.get('/blog',response_model=List[schemas.ShowBlog])
def all(db:Session= Depends(get_db), current_user:schemas.User=Depends(get_current_user)):
    blogs=db.query(models.Blog).all()
    return blogs


@router.get('/blog/{id}', status_code=200,response_model=schemas.ShowBlog )
def show(id,response:Response ,db:Session= Depends(get_db)):
    blog= db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        response.status_code=status.HTTP_404_NOT_FOUND
    return blog


@router.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED )
def update(id,request: schemas.Blog, db:Session= Depends(get_db)):
    
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    else:
        blog.update(request)
        db.commit()
        return 'updated'
    

@router.post('/blog')
def create(request:schemas.Blog, db:Session= Depends(get_db)):
    new_blog= models.Blog(title=request.title, body= request.body, user_id= 1)
    db.add(new_blog)
    
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT )
def destroy(id,db:Session= Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    else:
        blog.delete(synchronize_session=False)
        db.commit()
        return 'deleted'