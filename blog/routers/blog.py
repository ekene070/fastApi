from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, model, hashing, database # I use . because its in same directoryc
from ..repository import blog


router = APIRouter(
    prefix= "/blog",
    tags=["Blogs"]
)


@router.get("/", response_model=List[schemas.showBlog]) #We use List[schemas.showBlog] because we want a list and not just a single item,
def get_all_blogs(db: Session = Depends(database.get_db)):
    # blogs = db.query(model.Blog).all()
    # return blogs
    return blog.get_all(db)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog, db: Session = Depends(database.get_db)):
    # new_blog = model.Blog(title = request.title, body= request.body, creator_id = 1)
    # db.add(new_blog)
    # db.commit()
    # db.refresh(new_blog)
    # return new_blog
    return blog.create(request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(database.get_db)):
    # blog_to_delete = db.query(model.Blog).filter(model.Blog.id == id).delete(synchronize_session=False)
    # if not blog_to_delete:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    # db.commit()
    # return {f"Blog with id: {id} deleted successfully"}
    return blog.delete(id, db)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(database.get_db)):
    # # Create a dictionary of column-value pairs for the updates
    # update_data = {
    #     "title": request.title,
    #     "body": request.body
    # }
    # print(update_data)
    # # This will return the number of rows updated
    # rows_updated = db.query(model.Blog).filter(model.Blog.id == id).update(update_data)

    # if not rows_updated:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")

    # db.commit()
    # return {"message": "Blog updated successfully"}
    return blog.update(id, request, db)


@router.get("/{id}", status_code=200, response_model=schemas.showBlog) # We use response_model to get the particular info we need from the pydantic schema
def show(id, response:Response, db: Session = Depends(database.get_db)):
    # blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    # if not blog:
    #     raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not found")
    #     # response.status_code = status.HTTP_400_BAD_REQUEST
    #     # return {"detail": f"Blog with id {id} not found"}
    # return blog
    return blog.show(id, db)