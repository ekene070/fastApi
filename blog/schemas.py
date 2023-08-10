from pydantic import BaseModel


class Blog(BaseModel): # We need this cos we are trying to do a pydantic which is a sort of strict validation just like typescript does
    title: str
    body:str