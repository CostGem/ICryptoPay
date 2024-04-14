from enum import StrEnum


class CurrencyType(StrEnum):
    """Currency type"""

    CRYPTO: str = "crypto"
    FIAT: str = "fiat"
