from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Status(str, Enum):  # Structured result states
    SUCCESS = "success"
    NOT_FOUND = "not_found"
    RETRYABLE_ERROR = "retryable_error"


class CustomerLookupInput(BaseModel):  # Input Schema
    customer_id: str


class CustomerRecord(BaseModel):  # Output Schema
    customer_id: str
    name: str
    email: str


class CustomerLookupResult(BaseModel):
    status: Status
    customer: Optional[CustomerRecord] = None
    error_message: Optional[str] = None


def get_customer(input: CustomerLookupInput) -> CustomerLookupResult:  # Tool implementation
    """
    Tool name: get_customer
    Description: Retrieve a customer record by unique identifier.
    """
    database = {
        "cust_1": CustomerRecord(
            customer_id="cust_1",
            name="Asha Gupta",
            email="asha@example.com",
        )
    }
    record = database.get(input.customer_id)
    if record is None:
        return CustomerLookupResult(status=Status.NOT_FOUND)
    return CustomerLookupResult(status=Status.SUCCESS, customer=record)
