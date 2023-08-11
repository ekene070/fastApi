from pydantic import BaseModel


class Blog(BaseModel): # We need this cos we are trying to do a pydantic which is a sort of strict validation just like typescript does
    title: str
    body:str

class showBlog(BaseModel): #This will only show the exact body we need
    title: str
    body: str
    class Config(): # We use this because when we try to show this showBlog class, we need to have orm configured
        orm_mode = True

class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str
    
    class Config(): # We use this because when we try to show this showBlog class, we need to have orm configured
      orm_mode = True