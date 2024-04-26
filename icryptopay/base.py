import asyncio
import ssl
from asyncio import AbstractEventLoop
from typing import Optional

import certifi
from aiohttp import ClientSession, TCPConnector
from aiohttp.typedefs import StrOrURL

from icryptopay.enums.http import HTTPMethod
from icryptopay.exceptions import CryptoPayAPIError


class BaseClient:
    """Base aiohttp client"""

    __session: Optional[ClientSession] = None
    __loop: Optional[AbstractEventLoop] = None

    def __init__(self) -> None:
        self._loop = asyncio.get_event_loop()
        self._session = None

    def get_session(self, **kwargs) -> ClientSession:
        """Get cached session. One session per instance"""

        if isinstance(self._session, ClientSession) and not self._session.closed:
            return self._session

        ssl_context: ssl.SSLContext = ssl.create_default_context(cafile=certifi.where())
        connector: TCPConnector = TCPConnector(ssl=ssl_context)

        self._session = ClientSession(connector=connector, **kwargs)

        return self._session

    async def _make_request(self, url: StrOrURL, method: str = HTTPMethod.GET, **kwargs) -> dict:
        """
        Make a request.
            :param method: HTTP Method
            :param url: endpoint link
            :param kwargs: data, params, json and other...
            :return: status and result or exception
        """

        session: ClientSession = self.get_session()

        async with session.request(method=method, url=url, **kwargs) as response:
            response = await response.json(content_type="application/json")

        return self._validate_response(response)

    @staticmethod
    def _validate_response(response: dict) -> dict:
        """Validate response"""

        if not response.get("ok"):
            name = response["error"]["name"]
            code = response["error"]["code"]
            raise CryptoPayAPIError(code, name)
        return response

    async def close(self):
        """Close the session graceful."""

        if not isinstance(self._session, ClientSession):
            return

        if self._session.closed:
            return

        await self._session.close()
