from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

#database for user 
class User(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    name : str = Field(index=True)
    email : str = Field(unique=True)
    college : str

    #relationships
    # one user can have many books
    books: list["Book"]= Relationship(back_populates="owner") #When Python first reads the User class, the Book class hasn't been defined yet!

#request body for creating a user
class UserCreate(SQLModel):
    name:str
    email:str
    college:str

#response body 
class UserRead(SQLModel):
    id:str
    name:str
    email:str
    college:str

#avoid circular imports

from models.book import Book
User.model_rebuild() # model_rebuild : "Hey, remember that Book class I mentioned earlier? It exists now. Go back and make sure you understand what Book means."
    