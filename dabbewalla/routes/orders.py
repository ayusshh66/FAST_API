from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlmodel import  Session, select
from database import get_session
from models import orderStatus, Order,OrderUpdateStatus, StatusLog, OrderCreate

router = APIRouter(prefix="/orders", tags= ["orders"])

@router.post("/", response_model=Order)
def create_order(
    order : OrderCreate,
    session : Session= Depends(get_session)
):
    db_order = Order(**order.model_dump())
    session.add(db_order)
    session.commit()
    session.refresh(db_order)

    return db_order

@router.get("/{orderId}", response_model=list[Order])
def get_order(orderId:int | None = Query(None, description="order id from params"),
    status:orderStatus| None = Query(None, description="status id from params"),
    created_date:str | None = Query(None, description="date id from query"),
    limit : int | None = Query(10, ge=1,description="limit from queries"),
    offset : int | None = Query(0, ge=0,description="offeset from queries"),
    session : Session = Depends(get_session)):

        query = select(Order)

        if status:
            query = query.where(Order.status == status)

        if created_date :
            start = datetime.combine(created_date, datetime.min.time())
            end = datetime.combine(created_date, datetime.max.time())
            query = query.where(Order.created_at>= start, Order.created_at <= end)

        query = query.limit(limit).offset(offset)

        return session.exec(query).all()


    