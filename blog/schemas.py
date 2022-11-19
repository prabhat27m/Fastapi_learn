from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

class Blog(BaseModel):
    title :str
    body:str
    

#fastApi me pydantic model to schema bolte hai
# agar tumko sirf title aur body hi dikhana h to schema use karo nhi to models to sqlalchemy wala rhega hi


class User(BaseModel):
    name:str
    email:str
    password:str
    
    
class ShowUser(User):
    name:str
    email:str
    # blog:List[Blog]=[]
    class Config():
        orm_mode=True


class ShowBlog(Blog):
    title :str
    body:str
    creator:ShowUser
    
    class Config():
        orm_mode=True