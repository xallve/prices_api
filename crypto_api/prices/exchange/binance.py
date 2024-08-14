from .base import ExchangeWebSocket
import json
from .mixin.unifymixins import BinancePairMixin


class BinanceWebSocket(ExchangeWebSocket, BinancePairMixin):
    def __init__(self, pair=None):
        ExchangeWebSocket.__init__(self, 'wss://stream.binance.com:9443/ws', 'Binance')
        self.pair = self.unify_pair_name(pair).lower() if pair else None
        self.prices = {}
        print(self.pair)

    async def subscribe(self, websocket):

        subscribe_message = {
            "method": "SUBSCRIBE",
            "params": [f"{self.pair}@ticker"] if self.pair else ["!ticker@arr"],  # get prices for all symbols if needed
            "id": 1
        }
        await websocket.send(json.dumps(subscribe_message))

    async def process_message(self, message):
        data = json.loads(message)
        if data != {'result': None, 'id': 1}:
            # Handle prices data if no ticker is specified because it returns as list of dicts
            if isinstance(data, list):
                for ticker in data:
                    symbol = ticker['s']
                    price = (float(ticker['b']) + float(ticker['a'])) / 2  # Get average of Bst bid and Ask
                    self.prices[symbol] = price
                return {'Binance': self.prices}
            else:
                symbol = data['s']
                price = (float(data['b']) + float(data['a'])) / 2
                self.prices[symbol] = price
                return {symbol: price}
