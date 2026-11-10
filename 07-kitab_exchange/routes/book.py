
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from sqlmodel import Session, select, col

from models.book import BookRead, Book, BookCreate, BookUpdate
from database import get_session
from auth import verify_api


router = APIRouter(prefix="/book", tags=["books"])


@router.get("/", response_model=list[BookRead])
def get_books(
    title: Optional[str] = Query(default=None),
    author: Optional[str] = Query(default=None),
    session: Session = Depends(get_session)
):
    query = select(Book).where(col(Book.is_sold).is_(False))

    if title:
        query = query.where(col(Book.title).contains(title))

    if author:
        query = query.where(col(Book.author).contains(author))

    books = session.exec(query).all()

    return books


@router.post("/", response_model=BookRead)
def post_books(
    book_data: BookCreate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api)
):
    book = Book.model_validate(book_data)

    session.add(book)
    session.commit()
    session.refresh(book)

    return book


@router.patch("/{book_id}", response_model=BookRead)
def update_book(
    book_id: int,
    update_data: BookUpdate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api)
):
    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    book_data = update_data.model_dump(exclude_unset=True)

    for key, value in book_data.items():
        setattr(book, key, value)

    session.add(book)
    session.commit()
    session.refresh(book)

    return book


@router.patch("/{book_id}/sold", response_model=BookRead)
def sold_book(
    book_id: int,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api)
):
    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    book.is_sold = True

    session.add(book)
    session.commit()
    session.refresh(book)

    return book
