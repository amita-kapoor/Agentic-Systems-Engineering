from typing import Literal, Optional

from pydantic import BaseModel


class CustomerLookupInputV1(BaseModel):
    customer_id: str


class CustomerLookupResultV1(BaseModel):
    status: Literal["found", "not_found"]
    customer: Optional[dict] = None


class CustomerLookupInputV2(BaseModel):
    customer_id: str
    include_orders: bool = False


class CustomerLookupResultV2(BaseModel):
    status: Literal["found", "not_found"]
    customer: Optional[dict] = None
    recent_orders: list[dict] = []


class CustomerLookupToolV1:
    metadata = ToolMetadata(
        name="get_customer",
        description="Retrieve a customer record by unique identifier.",
        args_schema=CustomerLookupInputV1,
        version="1.0.0",
    )
    async def _run(self, input: CustomerLookupInputV1) -> CustomerLookupResultV1:  #A
        database = {"cust_1": {"name": "Asha Gupta", "email": "asha@example.com"}}
        record = database.get(input.customer_id)
        if record is None:
            return CustomerLookupResultV1(status="not_found")
        return CustomerLookupResultV1(status="found", customer=record)


class CustomerLookupToolV2:
    metadata = ToolMetadata(
        name="get_customer",
        description="Retrieve a customer record and optionally include recent orders.",
        args_schema=CustomerLookupInputV2,
        version="2.0.0",
    )

    async def _run(self, input: CustomerLookupInputV2) -> CustomerLookupResultV2:
        database = {"cust_1": {"name": "Asha Gupta", "email": "asha@example.com"}}
        record = database.get(input.customer_id)
        if record is None:
            return CustomerLookupResultV2(status="not_found")
        orders = [{"order_id": "ord_1", "amount": 49.99}] if input.include_orders else []
        return CustomerLookupResultV2(status="found", customer=record, recent_orders=orders)

#A Both versions execute, so the adapter in Listing 5.9 can call version 2
