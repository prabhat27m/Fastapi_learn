from fastapi import APIRouter, Depends,Response, status,HTTPException
from typing import List
from .. import schemas, models, database,hashing
from sqlalchemy.orm import Session

from ..database import get_db

router= APIRouter()




@router.post('/user' , tags=['Users'])
def create_user(request: schemas.User,db:Session= Depends(get_db)):
    
    new_user=models.User(name=request.name, email=request.email, password=hashing.get_password_hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/users',response_model=List[schemas.ShowUser] , tags=['Users'])
def all(db:Session= Depends(get_db)):
    users=db.query(models.User).all()
    return users

@router.delete('/user/{id}' , tags=['Users'])
def user_delete(id,db:Session= Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found")
    user.delete(synchronize_session=False)
    db.commit()
    return 'deleted'