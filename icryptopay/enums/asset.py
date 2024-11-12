from enum import StrEnum


class Asset(StrEnum):
    """Asset type enume"""

    BTC: str = "BTC"
    TON: str = "TON"
    ETH: str = "ETH"
    USDT: str = "USDT"
    USDC: str = "USDC"
    BNB: str = "BNB"
    TRX: str = "TRX"
    LTC: str = "LTC"
    GRAM: str = "GRAM"
    NOT: str = "NOT"
    MY: str = "MY"
    SOL: str = "SOL"

    @classmethod
    def values(cls):
        return list(map(lambda asset: asset.value, cls))
