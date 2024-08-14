from .base import ExchangeWebSocket
import json
from .mixin.unifymixins import KrakenPairMixin
from .kraken_pairs import KRAKEN_PAIRS


class KrakenWebSocket(ExchangeWebSocket, KrakenPairMixin):
    # Kraken is way worse than Binance unfortunately at least for this task
    def __init__(self, pair=None):
        ExchangeWebSocket.__init__(self, 'wss://ws.kraken.com', 'Kraken')
        self.pair = self.unify_pair_name(pair) if pair else KRAKEN_PAIRS

    async def subscribe(self, websocket):

        subscribe_message = {
            "event": "subscribe",
            "pair": self.pair if isinstance(self.pair, list) else [self.pair],
            "subscription": {"name": "ticker"}
        }
        await websocket.send(json.dumps(subscribe_message))

    async def process_message(self, message):
        """
        Pretty much a hack as well
        :param message: message from websocket
        :return: a list of symbol/price
        """
        data = json.loads(message)
        if not isinstance(data, dict):
            print(data)
            price = (float(data[1].get('a')[0]) + float(data[1].get('b')[0]))/2  # Get average of bid and ask
            symbol = data[-1]
            return {symbol: price}
