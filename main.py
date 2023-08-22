from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def index():
    return {
        "data": {
            "name": "Ekene",
        "age": 15
        }
    }

#In fastapi, we can use strict typing pattern as in typescript
@app.get("/blog")
def blog(limit=10, published: bool=True, sort:Optional[str] = None): # This is how we accept query parameter(?) in fastapi
    # Only get 10 published blogs
    if published:
        return {"data": f'{limit} published blogs from db'}
    else:
        return {"data": f'{limit} blogs from db'}


@app.get("/blog/{id}/comments")
def comment(id):
    return {"data": f'id {id} comments'}

class Blog(BaseModel):
    title: str
    body: str
    published_at: Optional[bool]
    

@app.post("/blog")
def create_blog(request : Blog):
    return {"data": f"Blog is created with {request.title}"}
