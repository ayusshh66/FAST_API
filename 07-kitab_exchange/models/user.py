from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

#database for user 
class User(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    name : str = Field(index=True)
    email : str = Field(unique=True)
    college : str
    
    