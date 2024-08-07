from typing import List, Union

from icryptopay.types.rates import ExchangeRate


def get_rate(source: str, target: str, rates: List[ExchangeRate]) -> ExchangeRate:
    """
    Get rate by source and target

    :param source: Source asset
    :param target: Target asset
    :param rates: List of exchange rates
    """

    for rate in rates:
        if rate.source == source and rate.target == target:
            return rate


def get_rate_summ(summ: Union[int, float], rate: ExchangeRate) -> Union[int, float]:
    """
    Get rate summ

    :param summ: summ
    :param rate: Rate
    """

    return summ / rate.rate
