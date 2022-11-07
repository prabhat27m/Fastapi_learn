from fastapi import FastAPI
from pydantic import BaseModel

class Blog(BaseModel):
    title :str
    body:str

#fastApi me pydantic model to schema bolte hai
# agar tumko sirf title aur body hi dikhana h to schema use karo nhi to models to sqlalchemy wala rhega hi
class ShowBlog(Blog):
    class Config():
        orm_mode=True


class User(BaseModel):
    name:str
    email:str
    password:str
    

