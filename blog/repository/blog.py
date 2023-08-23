from fastapi import status, HTTPException
from .. import schemas, model
from sqlalchemy.orm import Session


def get_all(db: Session):
    blogs = db.query(model.Blog).all()
    return blogs

def create(request:schemas.Blog, db: Session):
    new_blog = model.Blog(title = request.title, body= request.body, creator_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete(id, db: Session):
    blog_to_delete = db.query(model.Blog).filter(model.Blog.id == id).delete(synchronize_session=False)
    if not blog_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    db.commit()
    return {f"Blog with id: {id} deleted successfully"}

def update(id, request:schemas.Blog, db: Session):
        # Create a dictionary of column-value pairs for the updates
    update_data = {
        "title": request.title,
        "body": request.body
    }
    # This will return the number of rows updated
    rows_updated = db.query(model.Blog).filter(model.Blog.id == id).update(update_data)

    if not rows_updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")

    db.commit()
    return {"message": "Blog updated successfully"}


def show(id, db: Session):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    if not blog:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not found")
        # response.status_code = status.HTTP_400_BAD_REQUEST
        # return {"detail": f"Blog with id {id} not found"}
    return blog