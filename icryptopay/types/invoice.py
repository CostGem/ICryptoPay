from pydantic import BaseModel

from typing import Union, Optional, List, Literal
from datetime import datetime

from icryptopay.enums.button import PaidButton
from icryptopay.enums.asset import Asset
from icryptopay.enums.currency import CurrencyType
from icryptopay.enums.fiat import FiatType
from icryptopay.enums.invoice import InvoiceStatus


class Invoice(BaseModel):
    invoice_id: int
    hash: str
    currency_type: Union[CurrencyType, Literal["crypto", "fiat"]]
    asset: Optional[Union[Asset, str]] = None
    fiat: Optional[Union[FiatType, str]] = None
    amount: Union[int, float, str]
    paid_asset: Optional[Union[Asset, str]] = None
    paid_amount: Optional[Union[int, float]] = None
    paid_fiat_rate: Optional[str] = None
    accepted_assets: Optional[List[Union[Asset, str]]] = None
    fee_asset: Optional[Union[Asset, str]] = None
    fee_amount: Optional[Union[int, float]] = None
    fee_in_usd: Optional[Union[int, float]] = None
    bot_invoice_url: str
    mini_app_invoice_url: str
    web_app_invoice_url: str
    description: Optional[str] = None
    status: Union[InvoiceStatus, str]
    created_at: str
    paid_usd_rate: Optional[Union[int, float]] = None
    allow_comments: bool
    allow_anonymous: bool
    expiration_date: Optional[str] = None
    paid_at: Optional[datetime] = None
    paid_anonymously: Optional[bool] = None
    comment: Optional[str] = None
    hidden_message: Optional[str] = None
    payload: Optional[str] = None
    paid_btn_name: Optional[Union[PaidButton, str]] = None
    paid_btn_url: Optional[str] = None
