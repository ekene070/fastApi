from .. import schemas, model, hashing, database
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
