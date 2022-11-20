from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from .. import schemas, models,hashing
from ..database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..oauth2 import create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES

router= APIRouter(
    tags=['auth']
)

@router.post('/login')
def login( db:Session= Depends(get_db),request: OAuth2PasswordRequestForm = Depends()):
    user= db.query(models.User).filter(models.User.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User not found")
    
    if not hashing.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Incorrect password")
    
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}
