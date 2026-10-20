from sqlmodel import SQLModel, Field, table
from typing import Optional
from datetime import datetime

class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    play_name : str = Field(index=True)
    reviewer_name:str
    rating : int = Field(gt=1, le=5)
    comment : str 
    create_At :datetime = Field(default_factory=datetime.now)

class ReviewCreate(SQLModel):
    play_name:str
    reviewer_name : str
    rating : int = Field(gt=1, le=5)
    comment:str 



    