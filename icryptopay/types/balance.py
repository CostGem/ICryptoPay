from pydantic import BaseModel

from typing import Union

from icryptopay.enums.asset import Asset


class Balance(BaseModel):
    currency_code: Union[Asset, str]
    available: Union[float]
    onhold: Union[float]
