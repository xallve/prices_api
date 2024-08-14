import asyncio
from prices.exchange.binance import BinanceWebSocket
from prices.exchange.kraken import KrakenWebSocket


async def get_prices(pair=None, exchange=None):
    tasks = []

    if exchange in [None, 'binance']:
        binance_ws = BinanceWebSocket(pair)
        tasks.append(binance_ws.connect())

    if exchange in [None, 'kraken']:
        kraken_ws = KrakenWebSocket(pair)
        tasks.append(kraken_ws.connect())

    data = await asyncio.gather(*tasks)

    return data
