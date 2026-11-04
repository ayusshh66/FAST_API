from fastapi import APIRouter, Depends
from sqlmodel import  Session, select
from database import get_session
from models import orderStatus, Order,OrderUpdateStatus, StatusLog, OrderCreate 

router = APIRouter(prefix="/orders", tags= ["orders"])

@router.post("/orders", response_model=Order)
def create_order(
    order : OrderCreate,
    session : Session= Depends(get_session)
):
    db_order = Order(**order.model_dump())
    session.add(db_order)
    session.commit()
    session.refresh(db_order)

    return db_order
    