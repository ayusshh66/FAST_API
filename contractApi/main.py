
from fastapi import FastAPI, status
from random import randint

from data import orders_db

from exceptions import (
    invalid_orderId_handler,
    invalid_orderId,
    orderId_error_handler,
    orderId_error
)

from models import (
    BulkOrderReponse,
    BulkOrderRequest,
    CreateOrderRequest,
    OrderResponse
)

app = FastAPI(
    title="Contract API Project",
    description="Practice FastAPI CRUD, Pydantic models, and custom exceptions"
)


# CHANGE 1: Use add_exception_handler(), not exception_handlers()
app.add_exception_handler(invalid_orderId, invalid_orderId_handler)
app.add_exception_handler(orderId_error, orderId_error_handler)


# CHANGE 2: Return the dictionary directly
@app.get("/")
def get_all_orders():
    return orders_db


# CHANGE 3: POST bulk lookup instead of GET
# Pydantic request models are read from the JSON request body.
# IMPORTANT: Define /order/bulk before /order/{orderId}
@app.post("/order/bulk", response_model=BulkOrderReponse)
def get_bulk_orders(req: BulkOrderRequest):

    results = []
    missing = []

    for code in req.orderIds:
        if code in orders_db:
            results.append(orders_db[code])
        else:
            missing.append(code)

    return BulkOrderReponse(
        found=len(results),
        missing=len(missing),
        result=results,
        missing_order=missing
    )


# CHANGE 4: Removed f-string from the route
# Added response_model to validate the returned order
@app.get("/order/{orderId}", response_model=OrderResponse)
def get_order(orderId: str):

    # CHANGE 5: Check length AND whether ID contains only digits
    if len(orderId) != 6 or not orderId.isdigit():
        raise invalid_orderId(
            orderId,
            "Order ID must contain exactly 6 digits"
        )

    # Raise 404 if the ID is valid but doesn't exist
    if orderId not in orders_db:
        raise orderId_error(orderId)

    return orders_db[orderId]


# CHANGE 6: POST now creates and saves a new order
@app.post(
    "/order",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED
)
def post_order(req: CreateOrderRequest):

    # Generate a unique 6-digit order ID
    while True:
        order_id = str(randint(100000, 999999))

        if order_id not in orders_db:
            break

    # Pydantic has already validated req.
    # No manual type checking is required.

    # Create an order dictionary
    new_order = {
        "order_id": order_id,
        "order_name": req.order_name,
        "ordered_product": req.ordered_product,
        "quantity": req.quantity,
        "price": req.price
    }

    # Save the order to our in-memory database
    orders_db[order_id] = new_order

    # Return the created order
    return new_order
    