from fastapi import FastAPI

from data import orders_db

from exceptions import (invalid_orderId_handler, invalid_orderId, orderId_error_handler, orderId_error)

from models import (BulkOrderReponse, BulkOrderRequest, CreateOrderRequest, OrderIdRequest, OrderResponse)

app = FastAPI(
    title="contract api project",
    description="practicint past api CRUD, here user can post, get the order by their order ids"
)

app.exception_handlers(invalid_orderId, invalid_orderId_handler)
app.add_exception_handler(orderId_error, orderId_error_handler)

@app.get("/")
def getAllOrders():
    
    return data = {
        orders_db
    }

@app.get(f"/order/{orderId}")
def getOrder(orderId:str):
    if len(orderId) != 6 or not isinstance(orderId, str):
        raise invalid_orderId(orderId)

    if orderId not in orders_db:
        raise orderId_error(orderId)
    return orders_db[orderId]

# class CreateOrderRequest(BaseModel):
#     order_name: str = Field(min_length=2, max_length=100)
#     ordered_product: str = Field(min_length=2, max_length=100)
#     quantity: int = Field(gt=0)
#     price: float = Field(gt=0)

@app.post("/order")
def postOrder(req:CreateOrderRequest):
    order_name = req.order_name
    order_product = req.ordered_product
    quantity = req.quantity
    price = req.price

    if type(price) != float and type(quantity) != int :
        return {
            "error" : "the price and quantity should be in numbers"
        }
    return {
        order_name,
        order_product,
        quantity,
        price,
    }