from enum import StrEnum


class CheckStatus(StrEnum):
    """Check status"""

    ACTIVE: str = "active"
    ACTIVATED: str = "activated"
