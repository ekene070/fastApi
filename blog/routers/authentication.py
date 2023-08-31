from fastapi import APIRouter, Depends, status, Response, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, database, model, token
from sqlalchemy.orm import Session
from .. import hashing


router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    print( "user info")
    user = db.query(model.User).filter(model.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    if not hashing.Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
