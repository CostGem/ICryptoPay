from enum import StrEnum


class APIMethod(StrEnum):
    GET_ME: str = "/api/getMe"
    GET_STATS: str = "/api/getStats"
    GET_BALANCE: str = "/api/getBalance"
    GET_EXCHANGE_RATES: str = "/api/getExchangeRates"
    CREATE_INVOICE: str = "/api/createInvoice"
    GET_INVOICES: str = "/api/getInvoices"
    DELETE_INVOICE: str = "/api/deleteInvoice"
    TRANSFER: str = "/api/transfer"
    GET_TRANSFERS: str = "/api/getTransfers"
    CREATE_CHECK: str = "/api/createCheck"
    GET_CHECKS: str = "/api/getChecks"
    DELETE_CHECK: str = "/api/deleteCheck"
    GET_CURRENCIES: str = "/api/getCurrencies"
