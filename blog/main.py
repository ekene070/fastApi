from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, model # I use . because its in same directoryc
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

model.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog, db: Session = Depends(get_db)):
    new_blog = model.Blog(title = request.title, body= request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    blog_to_delete = db.query(model.Blog).filter(model.Blog.id == id).delete(synchronize_session=False)
    if not blog_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    db.commit()
    return {f"Blog with id: {id} deleted successfully"}

@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
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

@app.get("/blog")
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(model.Blog).all()
    return blogs

@app.get("/blog/{id}", status_code=200)
def show(id, response:Response, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    if not blog:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
        # response.status_code = status.HTTP_400_BAD_REQUEST
        # return {"detail": f"Blog with id {id} not found"}
    return blog
