from typing import Union

from pydantic import BaseModel

from icryptopay.enums.asset import Asset
from icryptopay.enums.fiat import FiatType


class ExchangeRate(BaseModel):
    is_valid: bool
    is_crypto: bool
    is_fiat: bool
    source: Union[Asset, FiatType]
    target: FiatType
    rate: Union[float]
