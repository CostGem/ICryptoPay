from pydantic import BaseModel
from datetime import datetime

from icryptopay.types.invoice import Invoice


class Update(BaseModel):
    update_id: int
    update_type: str
    request_date: datetime
    payload: Invoice
