import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor


class BinancePairMixin:
    """
    Mixin classes to unify pair param. E.g. for binance it should be
    btcusdt; But now user can specify param as BTC_USDT; BTC/USDT; and so on
    """
    def unify_pair_name(self, pair):
        unified_pair = ''.join(filter(str.isalnum, pair)).upper()
        unified_pair = (unified_pair.replace('/', '')
                        .replace('-', '')
                        .replace('_', '').upper())

        return unified_pair


class KrakenPairMixin:
    """
    E.G. btcusd -> BTC/USD
    """
    def unify_pair_name(self, pair):
        unified_pair = ''.join(filter(str.isalnum, pair)).upper()

        base_currency = unified_pair[:-3]
        quote_currency = unified_pair[-3:]

        formatted_pair = f'{base_currency}/{quote_currency}'

        return formatted_pair


def force_async(fn):
    """
    Decorator
    Turns a sync function nto an async function using threads
    """
    pool = ThreadPoolExecutor()

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        future = pool.submit(fn, *args, **kwargs)
        return asyncio.wrap_future(future)  # make it awaitable

    return wrapper