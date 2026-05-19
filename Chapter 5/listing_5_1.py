class Status(Enum):
    OK = "ok"
    NOT_FOUND = "not_found"
    AMBIGUOUS = "ambiguous"
class CustomerLookupResult:
    def __init__(self, status, customer=None, candidates=None):
        self.status = status
        self.customer = customer
        self.candidates = candidates
result = get_customer(customer_id) #A
if result.status == Status.OK:
    process_customer(result.customer)
elif result.status == Status.NOT_FOUND:
    ask_user_for_new_identifier()
elif result.status == Status.AMBIGUOUS:
    ask_user_to_select(result.candidates)
