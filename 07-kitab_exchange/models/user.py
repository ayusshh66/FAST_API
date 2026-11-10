
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


# Database model for User
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True)
    college: str

    # One user can have many books
    books: list["Book"] = Relationship(back_populates="owner")


# Request body for creating a user
class UserCreate(SQLModel):
    name: str
    email: str
    college: str


# Response model
class UserRead(SQLModel):
    id: int
    name: str
    email: str
    college: str
