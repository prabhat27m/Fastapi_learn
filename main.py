from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
# @app is decorator , get is operation , index is path function

app = FastAPI()

@app.get('/blog')
def index(limit=10, published: bool=True, sort:Optional[str]=None):
    # only 10 published blogs
    if published:
        return {"data":f"{limit} blogs from the list"}

@app.get('/blog/unpublished')
def unpublished():
    pass 

@app.get('/blog/{id}')
def show(id:str):
    return {"data": id}

@app.get('/blog/{id}/comments')
def comments(id:int,  ):
    return {'comments of blog id ': {1,2,3} }


class Blog(BaseModel):
    title:str
    body :str
    published_at:Optional[bool]
    

@app.post('/blog')
def create_blog(request: Blog):
    return {'data' : f"blog is created with title as {request.title}"}
    return "blog created"



