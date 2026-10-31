from sqlite3 import dbapi2
from fastapi import APIRouter, Depends, Quer
from sqlalchemy.sql.expression import desc
from sqlmodel import Session, select
from models import Review, ReviewCreate, ReviewRead, ReviewUpdate
from database import create_table, get_session

router = APIRouter(prefix="/reviews", tags = ["reviews"])

@router.post("/", response_model=ReviewRead)
def create_reviews(review: ReviewCreate, session : Session= Depends(get_session)):
    review_db = Review(**review.model_dump())
    session.add(review_db)
    session.commit()
    session.refresh(review_db)

@router.get("/", response_model=list[ReviewRead])
def get_reviews(
    play_name: str|None = Query(None, description = "playname from query"),
    skip : int = Query(0, ge=0, description="number of reviews to skip"),
    limit : int = Query(0, le=50, description="number of reviews to be get"),
    session: Session =  Depends(get_session)
):
    query=select(Review)

    if play_name:
        query = query.where(Review.play_name == play_name)

    query=query.offset(skip).limit(limit)

    reviews = session.exec(query).all()
    return reviews