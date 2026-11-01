from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select, func
from starlette.types import HTTPExceptionHandler
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

@router.get("/average/{play_name}")
def get_avg(
    play_name : str,
    session : Session = Depends(get_session)
):
    result = session.exec(
        select(func.avg(Review.rating), func.count(Review.id)).where(Review.play_name == play_name)
    ).first()

    avg_rating, tota_reviews = result

    if tota_reviews == 0:
        raise HTTPException(status_code=404, detail = "no review found")

    return {
        "play_name"  : play_name,
        "average_rating" : round(avg_rating,2),
        "total_revies" : tota_reviews
    }

@router.get("/{review_id}", response_model=ReviewRead)
def get_review(
    session: Session= Depends(get_session),
    review_id:int
):
    result = session.get(Review, review_id) # .get(table, any coloum which is a primary key) in my case teh sno. is  primary key, so it will return only 1 data and wont query again adn aagain on calling
    if not result :
        raise HTTPException(status_code=404, detail=f"no review found with {review_id}")

    return result

    