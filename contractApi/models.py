from pydantic import BaseModel, field_validator

class OrderIdRequest(BaseModel):
    orderId=str

    @field_validator("orderId")
    @classmethod
    def validate_orderId(cls,value):
        if len(value) != 6 or not value.isinstance(value,str):
            raise ValueError("the order must be in string and of 6 characters")
        return value

