from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from sqlmodel import Session, select
from models.book import BookRead, Book, BookCreate, BookUpdate
from database import get_session
from auth import verify_api

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

@router.post("/",response_model=BookRead)
def post_books(
    book_data : BookCreate,
    session : Session=Depends(get_session),
    api_key: str =Depends(verify_api)
):
    books = Book.model_validate(book_data)
    session.add(books)
    session.commit()
    session.refresh(books)
    return books

@router.patch("/{book_id}", response_model=BookRead)
def update_book(
    book_id : int,
    update_data : BookUpdate,
    session : Session = Depends(get_session),
    api_key: str = Depends(verify_api)
):
    book = session.get(Book,book_id)

    if not book:
        raise HTTPException(status_code=404, detail="book not found")

    book_data = update_data.model_dump(exclude_unset=True)
    for key,value in book_data.items():
        setattr(book,key,value)

    session.add(book)
    session.commit()
    session.refresh(book)

    return book
    
@router.patch("/{book_id}/sold",response_model=BookRead)
def sold_book(
    book_id:int,
    session : Session = Depends(get_session),
    api_key: str = Depends(verify_api)
):
    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="book not found")

    book.is_sold = True

    session.add(book)
    session.commit()
    session.refresh(book)

    return book
    