from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Status(str, Enum):  #A
    SUCCESS = "success"
    NOT_FOUND = "not_found"
    RETRYABLE_ERROR = "retryable_error"


class CustomerLookupInput(BaseModel):  #B
    customer_id: str


class CustomerRecord(BaseModel):  #C
    customer_id: str
    name: str
    email: str


class CustomerLookupResult(BaseModel):
    status: Status
    customer: Optional[CustomerRecord] = None
    error_message: Optional[str] = None


CUSTOMERS = {
    "cust_1": CustomerRecord(
        customer_id="cust_1",
        name="Asha Gupta",
        email="asha@example.com"
    )
}



def get_customer(input: CustomerLookupInput, database= CUSTOMERS) -> CustomerLookupResult:  #D
    """
    Tool name: get_customer
    Description: Retrieve a customer record by unique identifier.
    """
    try:
        record = database.get(input.customer_id)
    except ConnectionError as e: #E
        return CustomerLookupResult(status=Status.RETRYABLE_ERROR, error_message=str(e))
    if record is None: #F
        return CustomerLookupResult(status=Status.NOT_FOUND)
    return CustomerLookupResult(status=Status.SUCCESS, customer=record)

#A Structured result states
#B Input Schema
#C Output Schema
#D Tool implementation 
#E The dependency failed; the caller may retry 
#F The dependency worked and the record does not exist; retrying will not help
