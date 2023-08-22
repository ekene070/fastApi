from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import List
from . import schemas, model, hashing # I use . because its in same directoryc
from .database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

model.Base.metadata.create_all(bind=engine) # This means anytime you find any model created, create it also on the database

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["blog"])
def create(request:schemas.Blog, db: Session = Depends(get_db)):
    new_blog = model.Blog(title = request.title, body= request.body, creator_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blog"])
def destroy(id, db: Session = Depends(get_db)):
    blog_to_delete = db.query(model.Blog).filter(model.Blog.id == id).delete(synchronize_session=False)
    if not blog_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    db.commit()
    return {f"Blog with id: {id} deleted successfully"}

@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blog"])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    # Create a dictionary of column-value pairs for the updates
    update_data = {
        "title": request.title,
        "body": request.body
    }
    print(update_data)
    # This will return the number of rows updated
    rows_updated = db.query(model.Blog).filter(model.Blog.id == id).update(update_data)

    if not rows_updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")

    db.commit()
    return {"message": "Blog updated successfully"}

@app.get("/blog", response_model=List[schemas.showBlog], tags=["blog"]) #We use List[schemas.showBlog] because we want a list and not just a single item,
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(model.Blog).all()
    return blogs

@app.get("/blog/{id}", status_code=200, response_model=schemas.showBlog, tags=["blog"]) # We use response_model to get the particular info we need from the pydantic schema
def show(id, response:Response, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    if not blog:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not found")
        # response.status_code = status.HTTP_400_BAD_REQUEST
        # return {"detail": f"Blog with id {id} not found"}
    return blog

#Create user profile
@app.post("/user",  response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(request:schemas.User, db: Session = Depends(get_db)):
    new_user = model.User(name = request.name, email = request.email, password = hashing.Hash.encrypt_password(request.password))
    print(new_user, "before create user")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/user/{id}", response_model=schemas.ShowUser, tags=["users"])
def get_user(id: int, db: Session = Depends(get_db)):
    users = db.query(model.User).filter(model.User.id == id).first()
    print(id, users, "before create user")
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not found")
    return users