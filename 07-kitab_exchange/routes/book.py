from fastapi import APIRouter, Depends, Query
from typing import Optional
from sqlmodel import Session, select
from models.book import BookRead, Book, BookCreate
from database import get_session

router = APIRouter(prefix="/book", tags=["books"])

@router.get("/", response_model=list[BookRead])
def get_books(
    title: Optional[str] = Query(default=None),
    author : Optional[str] = Query(default=None),
    session : Session = Depends(get_session)
):
    query = select(Book).where(Book.is_sold == False)

    if title:
        query = query.where(Book.title.contains(title))

    if author:
        query = query.where(Book.title.contains(author))    

    books = session.exec(query).all()

    return books
    