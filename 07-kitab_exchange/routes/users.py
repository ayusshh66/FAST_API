
from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session, select

from auth import verify_api
from models.user import User, UserCreate, UserRead
from database import get_session


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserRead, status_code=201)
def register_user(
    user_data: UserCreate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api)
):
    existing = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="User already registered"
        )

    result = User.model_validate(user_data)

    session.add(result)
    session.commit()
    session.refresh(result)

    return result


@router.get("/", response_model=list[UserRead])
def get_user_list(
    session: Session = Depends(get_session)
):
    return session.exec(select(User)).all()
