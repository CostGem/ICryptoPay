from datetime import datetime
from hashlib import sha256
from hmac import HMAC
from typing import Optional, Union, List, Callable, Dict, Any

from fastapi.openapi.models import Response
from starlette.requests import Request
from starlette.responses import JSONResponse

from icryptopay.enums.button import PaidButton
from icryptopay.enums.method import APIMethod
from icryptopay.base import BaseClient
from icryptopay.enums.asset import Asset
from icryptopay.enums.check import CheckStatus
from icryptopay.enums.currency import CurrencyType
from icryptopay.enums.http import HTTPMethod
from icryptopay.enums.invoice import InvoiceStatus
from icryptopay.enums.network import NetworkType
from icryptopay.types.app_stats import AppStats
from icryptopay.types.balance import Balance
from icryptopay.types.check import Check
from icryptopay.types.currencies import Currency
from icryptopay.types.invoice import Invoice
from icryptopay.types.profile import Profile
from icryptopay.types.rates import ExchangeRate
from icryptopay.types.transfer import Transfer
from icryptopay.types.update import Update
from icryptopay.utils.exchange import get_rate, get_rate_summ


class ICryptoPay(BaseClient):
    """ICryptoPay API client"""

    __network: NetworkType = NetworkType.MAIN
    __headers: Dict[str, Any] = {}
    __handlers = []

    def __init__(self, token: str, use_test_network: bool = False) -> None:
        super().__init__()

        self.__token = token

        if use_test_network:
            self.__network = NetworkType.TEST

        self.__headers["Crypto-Pay-API-Token"] = token

    async def __aenter__(self) -> None:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    def _build_request_url(self, method: APIMethod) -> str:
        """
        Returns a URL for the request

        :param method: API method
        """

        return self.__network + method

    async def get_me(self) -> Profile:
        """
        Use this method to test your app's authentication token. Requires no parameters.
        On success, returns basic information about an app.
        https://help.crypt.bot/crypto-pay-api#getMe
        """

        response = await self._make_request(
            method=HTTPMethod.GET,
            url=self._build_request_url(method=APIMethod.GET_ME),
            headers=self.__headers
        )

        return Profile(**response["result"])

    async def get_stats(
            self,
            start_at: Optional[Union[datetime, str]] = None,
            end_at: Optional[Union[datetime, str]] = None
    ) -> AppStats:
        """
        Use this method to get app statistics.
        http://help.crypt.bot/crypto-pay-api#jvP3

        :param start_at: Start date
        :param end_at: End date
        """

        params: Dict[str, Optional[Union[datetime, str]]] = {
            "start_at": start_at,
            "end_at": end_at
        }

        for key, value in params.copy().items():
            if isinstance(value, datetime):
                params[key] = str(value)
            if value is None:
                del params[key]

        response = await self._make_request(
            method=HTTPMethod.GET,
            url=self._build_request_url(method=APIMethod.GET_STATS),
            params=params,
            headers=self.__headers
        )

        return AppStats(**response["result"])

    async def get_balance(self) -> List[Balance]:
        """
        Use this method to get a balance of your app.
        https://help.crypt.bot/crypto-pay-api#getBalance
        """

        response = await self._make_request(
            method=HTTPMethod.GET,
            url=self._build_request_url(method=APIMethod.GET_BALANCE),
            headers=self.__headers
        )

        return [Balance(**balance) for balance in response["result"]]

    async def get_exchange_rates(self) -> List[ExchangeRate]:
        """
        Use this method to get exchange rates of supported currencies. Returns array of currencies.
        https://help.crypt.bot/crypto-pay-api#getExchangeRates
        """

        response = await self._make_request(
            method=HTTPMethod.GET,
            url=self._build_request_url(method=APIMethod.GET_EXCHANGE_RATES),
            headers=self.__headers
        )

        return [ExchangeRate(**rate) for rate in response["result"]]

    async def get_currencies(self) -> List[Currency]:
        """
        Use this method to get a list of supported currencies. Returns array of currencies.
        https://help.crypt.bot/crypto-pay-api#getCurrencies
        """

        response = await self._make_request(
            method=HTTPMethod.GET,
            url=self._build_request_url(method=APIMethod.GET_CURRENCIES),
            headers=self.__headers
        )

        return [Currency(**currency) for currency in response["result"]]

    async def create_invoice(
            self,
            amount: Union[int, float],
            asset: Optional[Union[Asset, str, List[Asset]]] = None,
            description: Optional[str] = None,
            hidden_message: Optional[str] = None,
            paid_btn_name: Optional[Union[PaidButton, str]] = None,
            paid_btn_url: Optional[str] = None,
            payload: Optional[str] = None,
            allow_comments: Optional[bool] = None,
            allow_anonymous: Optional[bool] = None,
            expires_in: Optional[int] = None,
            fiat: Optional[str] = None,
            currency_type: Optional[Union[CurrencyType, str]] = None,
            accepted_asset: Optional[Union[List[Union[Asset, str]], str]] = None,
    ) -> Invoice:
        """
        Use this method to create a new invoice.
        https://help.crypt.bot/crypto-pay-api#createInvoice

        :param amount: Invoice amount
        :param asset: Invoice asset
        :param description: Invoice description
        :param hidden_message: Invoice hidden message
        :param paid_btn_name: Paid button name
        :param paid_btn_url: Paid button URL
        :param payload: Invoice payload
        :param allow_comments: Allow comments
        :param allow_anonymous: Allow anonymous comments
        :param expires_in: Invoice expiration time
        :param fiat: Fiat currency
        :param currency_type: Currency type
        :param accepted_asset: Accepted asset
        """

        if accepted_asset and isinstance(accepted_asset, list):
            accepted_asset = ",".join(asset for asset in accepted_asset)

        params: Dict[str, Union[str, int, float, bool]] = {
            "asset": asset,
            "amount": amount,
            "description": description,
            "hidden_message": hidden_message,
            "paid_btn_name": paid_btn_name,
            "paid_btn_url": paid_btn_url,
            "payload": payload,
            "allow_comments": allow_comments,
            "allow_anonymous": allow_anonymous,
            "expires_in": expires_in,
            "fiat": fiat,
            "currency_type": currency_type,
            "accepted_assets": accepted_asset,
        }

        for key, value in params.copy().items():
            if isinstance(value, bool):
                params[key] = str(value).lower()
            if value is None:
                del params[key]

        print(params)

        response = await self._make_request(
            method=HTTPMethod.GET,
            url=self._build_request_url(method=APIMethod.CREATE_INVOICE),
            params=params,
            headers=self.__headers
        )

        return Invoice(**response["result"])

    async def get_invoices(
            self,
            asset: Optional[Union[Asset, str]] = None,
            invoice_ids: Optional[Union[List[int], int]] = None,
            status: Optional[Union[InvoiceStatus, str]] = None,
            offset: Optional[int] = None,
            count: Optional[int] = None
    ) -> Optional[Union[Invoice, List[Invoice]]]:
        """
        Use this method to get invoices of your app.
        https://help.crypt.bot/crypto-pay-api#getInvoices

        :param asset: Asset
        :param invoice_ids: List of invoice IDs
        :param status: Status
        :param offset: Offset
        :param count: Count
        """

        if invoice_ids and isinstance(invoice_ids, list):
            invoice_ids = ",".join(map(str, invoice_ids))

        params: Dict[str, Union[str, int]] = {
            "asset": asset,
            "invoice_ids": invoice_ids,
            "status": status,
            "offset": offset,
            "count": count
        }

        for key, value in params.copy().items():
            if value is None:
                del params[key]

        response = await self._make_request(
            method=HTTPMethod.GET,
            url=self._build_request_url(method=APIMethod.GET_INVOICES),
            params=params,
            headers=self.__headers
        )

        return [Invoice(**invoice) for invoice in response["result"]["items"]]

    async def delete_invoice(self, invoice_id: int) -> bool:
        """
        Use this method to delete invoices created by your app.
        http://help.crypt.bot/crypto-pay-api#34Hd
        """

        params: Dict[str, int] = {"invoice_id": invoice_id}

        response = await self._make_request(
            method=HTTPMethod.GET,
            url=self._build_request_url(method=APIMethod.DELETE_INVOICE),
            params=params,
            headers=self.__headers
        )

        return response["result"]

    async def transfer(
            self,
            user_id: int,
            asset: Union[Asset, str],
            amount: Union[int, float],
            spend_id: Union[str, int],
            comment: Optional[str] = None,
            disable_send_notification: Optional[bool] = None,
    ) -> Transfer:
        """
        Use this method to send coins from your app's balance to a user.
        https://help.crypt.bot/crypto-pay-api#transfer

        :param user_id: User ID
        :param asset: Asset
        :param amount: Amount
        :param spend_id: Spend ID
        :param comment: Comment
        :param disable_send_notification: Disable send notification
        """

        params: Dict[str, Union[str, int, float]] = {
            "user_id": user_id,
            "asset": asset,
            "amount": amount,
            "spend_id": spend_id,
            "comment": comment,
            "disable_send_notification": disable_send_notification,
        }

        for key, value in params.copy().items():
            if isinstance(value, bool):
                params[key] = str(value).lower()
            if value is None:
                del params[key]

        response = await self._make_request(
            method=HTTPMethod.GET,
            url=self._build_request_url(method=APIMethod.TRANSFER),
            params=params,
            headers=self.__headers
        )

        return Transfer(**response["result"])

    async def get_transfers(
            self,
            asset: Optional[Union[Asset, str]] = None,
            transfer_ids: Optional[Union[List[int], int]] = None,
            offset: Optional[int] = None,
            count: Optional[int] = None,
    ) -> List[Transfer]:
        """
        Use this method to get transfers created by your app.
        http://help.crypt.bot/crypto-pay-api#RjDU

        :param asset: Asset
        :param transfer_ids: List of transfer IDs
        :param offset: Offset
        :param count: Count
        """

        if transfer_ids and isinstance(transfer_ids, list):
            transfer_ids = ",".join(map(str, transfer_ids))

        params: Dict[str, Union[str, int]] = {
            "asset": asset,
            "transfer_ids": transfer_ids,
            "offset": offset,
            "count": count,
        }

        for key, value in params.copy().items():
            if value is None:
                del params[key]

        response = await self._make_request(
            method=HTTPMethod.GET,
            url=self._build_request_url(method=APIMethod.GET_TRANSFERS),
            params=params,
            headers=self.__headers
        )

        return [Transfer(**transfer) for transfer in response["result"]["items"]]

    async def create_check(
            self,
            asset: Union[Asset, str],
            amount: Union[int, float],
            pin_to_user_id: Optional[int] = None,
            pin_to_username: Optional[str] = None,
    ) -> Check:
        """
        Use this method to create a new check.
        http://help.crypt.bot/crypto-pay-api#ZU9K

        :param asset: Asset
        :param amount: Amount
        :param pin_to_user_id: Pin to user ID
        :param pin_to_username: Pin to username
        """

        params: Dict[str, Union[str, int, float]] = {
            "asset": asset,
            "amount": amount,
            "pin_to_user_id": pin_to_user_id,
            "pin_to_username": pin_to_username,
        }

        for key, value in params.copy().items():
            if value is None:
                del params[key]

        response = await self._make_request(
            method=HTTPMethod.GET,
            url=self._build_request_url(method=APIMethod.CREATE_CHECK),
            params=params,
            headers=self.__headers
        )

        return Check(**response["result"])

    async def get_checks(
            self,
            asset: Optional[Union[Asset, str]] = None,
            check_ids: Optional[Union[List[int], int]] = None,
            status: Optional[Union[CheckStatus, str]] = None,
            offset: Optional[int] = None,
            count: Optional[int] = None
    ) -> List[Check]:
        """
        Use this method to get checks created by your app
        http://help.crypt.bot/crypto-pay-api#nIwG

        :param asset: Asset
        :param check_ids: List of check IDs
        :param status: Status
        :param offset: Offset
        :param count: Count
        """

        if check_ids and isinstance(check_ids, list):
            check_ids = ",".join(map(str, check_ids))

        params: Dict[str, Union[str, int]] = {
            "asset": asset,
            "check_ids": check_ids,
            "status": status,
            "offset": offset,
            "count": count,
        }

        for key, value in params.copy().items():
            if value is None:
                del params[key]

        response = await self._make_request(
            method=HTTPMethod.GET,
            url=self._build_request_url(method=APIMethod.GET_CHECKS),
            params=params,
            headers=self.__headers
        )

        return [Check(**check) for check in response["result"]["items"]]

    async def delete_check(self, check_id: int) -> bool:
        """
        Use this method to delete checks created by your app.
        http://help.crypt.bot/crypto-pay-api#nd2L

        :param check_id: Check ID
        """

        response = await self._make_request(
            method=HTTPMethod.GET,
            url=self._build_request_url(method=APIMethod.DELETE_CHECK),
            params={"check_id": check_id},
            headers=self.__headers
        )

        return response["result"]

    def __verify_signature(self, body_text: str, crypto_pay_signature: str) -> bool:
        """
        Check the signature for webhook updates
        https://help.crypt.bot/crypto-pay-api#verifying-webhook-updates

        :param body_text: Body text
        :param crypto_pay_signature: Crypto-Pay-Api-Signature header
        """

        token: bytes = sha256(string=self.__token.encode("UTF-8")).digest()
        signature: str = HMAC(
            key=token,
            msg=body_text.encode("UTF-8"),
            digestmod=sha256
        ).hexdigest()

        return signature == crypto_pay_signature

    async def get_updates(self, request: Request) -> JSONResponse:
        """WebHook updates route"""
        update: Optional[Update] = await self.verify_update(request=request)

        if update:
            for handler in self.__handlers:
                handler(update)

        return self.get_ok_response()

    async def verify_update(self, request: Request) -> Optional[Update]:
        """Verify Webhook update"""

        body: Dict[str, Any] = await request.json()
        body_text: str = (await request.body()).decode("UTF-8")
        crypto_pay_signature: str = request.headers.get("Crypto-Pay-Api-Signature", "No value")
        signature: bool = self.__verify_signature(
            body_text=body_text,
            crypto_pay_signature=crypto_pay_signature
        )

        if signature:
            return Update(**body)

    @staticmethod
    def get_ok_response() -> JSONResponse:
        return JSONResponse(content={"msg": "Status OK!"})

    async def get_amount_by_fiat(
            self,
            summ: Union[int, float],
            asset: Union[Asset, str],
            target: str
    ) -> Union[int, float]:
        """Get amount in crypto by fiat summ"""

        rates = await self.get_exchange_rates()
        rate = get_rate(source=asset, target=target, rates=rates)
        fiat_summ = get_rate_summ(summ=summ, rate=rate)
        return fiat_summ

    def register_pay_handler(self, func: Callable) -> None:
        """Register handler when invoice paid"""

        self.__handlers.append(func)

    def pay_handler(self, func: Callable = None):
        def decorator(handler):
            self.__handlers.append(handler)
            return handler

        return decorator
