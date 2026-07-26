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


class CustomerLookupToolV2:
    metadata = ToolMetadata(
        name="get_customer",
        description="Retrieve a customer record and optionally include recent orders.",
        args_schema=CustomerLookupInputV2,
        version="2.0.0",
    )
