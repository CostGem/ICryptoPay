from pydantic import BaseModel

from typing import Union, Optional

from enums.asset import Asset
from enums.fiat import FiatType


class ExchangeRate(BaseModel):
    is_valid: bool
    is_crypto: bool
    is_fiat: bool
    source: Union[Asset, str]
    target: Union[FiatType, str]
    rate: Union[float]
