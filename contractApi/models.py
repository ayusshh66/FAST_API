from pydantic import BaseModel, field_validator

class OrderIdRequest(BaseModel):
    orderId=str

    @field_validator("orderId")
    @classmethod
    def validate_orderId(cls,value):
        if len(value) != 6 or not value.isinstance(value,str):
            raise ValueError("the order must be in string and of 6 characters")
        return value

class OrderResponse(BaseModel):
    order_id=str
    order_name: str
    ordered_product: str
    quantity: int
    price: float

class BulkOrderRequest(BaseModel):
    orderIds = []

    @field_validator("orderIds")
    @classmethod
    def validate_BulkOrderIds(cls,values):
        if len(values) == 0:
            raise ValueError("there should be atleast 1 orderId")
        if len(values)>20:
            raise ValueError("orderIds must not exceed more than 20")


        for code in values:
            if len(code) != 6 or not code.isinstance(code,str):
                raise ValueError("the orderId must be of 6charaters")
        return values