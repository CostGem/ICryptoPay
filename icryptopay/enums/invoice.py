from enum import StrEnum


class InvoiceStatus(StrEnum):
    """Invoice status"""

    ACTIVE: str = "active"
    PAID: str = "paid"
    EXPIRED: str = "expired"
