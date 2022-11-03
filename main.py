from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {"name ":"prabhat"}

@app.get('/about')
def about():
    return {"about": "Hello World!"}