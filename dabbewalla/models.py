from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional

#orderstatus (enum) -> preparing, picked_up, in_transit, delivered

class orderStatus(str, Enum):
    PREPARING = "preparing",
    PICKED_UP = "picked_up",
    IN_TRANSIT = "in_transit",
    DELVIERED = "delivered"


class Order(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key = True)
    customer_name : str
    delivery_address : str
    items : str
    status : orderStatus = Field(default=orderStatus.PREPARING)
    created_at : datetime = Field(default_factory=datetime.now)
    updated_at : datetime = Field(default_factory=datetime.now)

class OrderUpdateStatus(SQLModel):
    status: Optional[orderStatus] = None
    delivery_address : Optional[str] = None

class StatusLog(SQLModel):
    order_id:str
    old_status:str
    new_status:str
    changes_at:datetime
    