import asyncio

from .base import ExchangeWebSocket
import json
from .mixin.unifymixins import KrakenPairMixin, force_async
from .kraken_pairs import KRAKEN_PAIRS


class KrakenWebSocket(ExchangeWebSocket, KrakenPairMixin):
    # Kraken is way worse than Binance unfortunately at least for this task
    def __init__(self, pair=None):
        ExchangeWebSocket.__init__(self, 'wss://ws.kraken.com', 'Kraken')
        self.pair = self.unify_pair_name(pair) if pair else KRAKEN_PAIRS
        self.known_pairs = set()
        self.known_properties = set()
        self.prices = {}

    async def subscribe(self, websocket):

        subscribe_message = {
            "event": "subscribe",
            "pair": self.pair if isinstance(self.pair, list) else [self.pair],
            "subscription": {"name": "ticker"}
        }
        await websocket.send(json.dumps(subscribe_message))

    def price_aggregator(self, message):
        data = json.loads(message)
        if not isinstance(data, dict) and len(data) > 1:
            price = (float(data[1].get('a')[0]) + float(data[1].get('b')[0])) / 2  # Get average of bid and ask
            symbol = data[-1]
            if symbol not in self.known_pairs:
                self.known_pairs.add(symbol)
                self.prices[symbol] = price
            if isinstance(self.pair, list):
                if len(self.known_pairs) > 50:
                    return self.prices
            else:
                return self.prices

    async def process_message(self, message):
        """
        Pretty much a hack as well
        :param message: message from websocket
        :return: a list of symbol/price
        """
        try:
            result = await asyncio.wait_for(asyncio.to_thread(self.price_aggregator, message), timeout=20)
            return result
        except TimeoutError:
            return {'Kraken': self.prices}
