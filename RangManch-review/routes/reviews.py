from sqlite3 import dbapi2

from fastapi import APIRouter, Depends
from sqlmodel import Session
from models import Review, ReviewCreate, ReviewRead, ReviewUpdate
from database import create_table, get_session

router = APIRouter(prefix="/reviews", tags = ["reviews"])

@router.post("/", response_model=ReviewRead)
def create_reviews(review: ReviewCreate, session : Session= Depends(get_session)):
    review_db = Review(**review.model_dump())
    session.add(review_db)
    session.commit()
    session.refresh(review_db)