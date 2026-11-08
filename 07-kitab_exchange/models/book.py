from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class Book(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    title : str =  Field(index=True)
    author :str = Field(index=True)
    price: int
    is_sold : bool = Field(default=False)