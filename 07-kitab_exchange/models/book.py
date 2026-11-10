from optparse import Option

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class Book(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    title : str =  Field(index=True)
    author :str = Field(index=True)
    price: int
    is_sold : bool = Field(default=False)

    #Foreign key
    user_id : int = Field(foreign_key="user.id")
        

    from models.user import User
    owner: Optional["User"] = Relationship(back_populates="owner")

# request body to create a book

class BookCreate(SQLModel):
    title:str
    auther:str
    price:str   
    user_id:int

class BookRead(SQLModel):
    id:int
    title:str
    author:str
    price:int
    is_sold:bool
    user_id:int

class BookUpdate(SQLModel):
    price : Optional[int] = None
    is_sold: Optional[bool] = None

from models.user import User
Book.model_rebuild()