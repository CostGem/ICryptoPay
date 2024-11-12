from enum import StrEnum


class NetworkType(StrEnum):
    """Cryptobot networks"""

    MAIN: str = "https://pay.crypt.bot"
    TEST: str = "https://testnet-pay.crypt.bot"
