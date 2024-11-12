from pydantic import BaseModel

from typing import Union, Optional
from datetime import datetime

from icryptopay.enums.asset import Asset


class Transfer(BaseModel):
    transfer_id: int
    user_id: int
    asset: Union[Asset, str]
    amount: Union[int, float]
    status: str
    completed_at: datetime
    comment: Optional[str] = None
