from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, model, hashing, database # I use . because its in same directoryc
from ..repository import user


router = APIRouter(
    prefix= "/user",
    tags=["Users"]
)

@router.post("/",  response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request:schemas.User, db: Session = Depends(database.get_db)):
    # new_user = model.User(name = request.name, email = request.email, password = hashing.Hash.encrypt_password(request.password))
    # db.add(new_user)
    # db.commit()
    # db.refresh(new_user)
    # return new_user
    return user.create(request, db)

@router.get("/{id}", response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(database.get_db)):
    print(id, "before get user")
    users = db.query(model.User).filter(model.User.id == id).first()
    print(id, users, "before create user")
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not found")
    return users
