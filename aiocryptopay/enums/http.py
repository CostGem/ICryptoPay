from enum import StrEnum


class HTTPMethod(StrEnum):
    """Available HTTP methods"""

    POST: str = "POST"
    GET: str = "GET"
