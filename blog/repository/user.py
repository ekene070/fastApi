from fastapi import status, HTTPException
from .. import schemas, model, hashing
from sqlalchemy.orm import Session


def create(request:schemas.ShowUser, db: Session):
    new_user = model.User(name = request.name, email = request.email, password = hashing.Hash.encrypt_password(request.password))
    print("Creating new user: ", new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def getOneUser(db: Session):
    users = db.query(model.User).filter(model.User.id == id).first()
    print(id, users, "before create user")
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not found")
    return users