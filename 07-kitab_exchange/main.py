from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session, select
from auth import verify_api
from models.user import    User, UserCreate, UserRead
from database import get_session

router = APIRouter("/users", tags=["users"])

@router.get("/", response_model=UserRead)
def register_user(user_Data: UserCreate, session: Session = Depends(get_session),
    api_key: str= Depends(verify_api)):

        existing = session.exec(
            select(User).where(User.email == user_Data.email)
        ).first()

        if existing :
            raise HTTPException(status_code=400, detail="user already registered")

        result = User.model_validate(user_Data)

        session.add(result)
        session.commit()
        session.refresh(result)


        return user