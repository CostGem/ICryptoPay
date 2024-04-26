from enum import StrEnum


class PaidButton(StrEnum):
    """Cryptobot paid button names"""

    VIEW_ITEM: str = "viewItem"
    OPEN_CHANNEL: str = "openChannel"
    OPEN_BOT: str = "openBot"
    CALLBACK: str = "callback"
