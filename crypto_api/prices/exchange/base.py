import websockets


class ExchangeWebSocket:
    """
    Encapsulate connection logic to base class
    """
    def __init__(self, uri, exchange_name):
        self.uri = uri
        self.exchange_name = exchange_name
        self.prices = {}

    async def connect(self):
        async with websockets.connect(self.uri) as websocket:
            await self.subscribe(websocket)
            retrieved_data = await self.receive_data(websocket)
            return retrieved_data

    async def subscribe(self, websocket):
        """Override this method in child classes to send subscription messages"""
        raise NotImplementedError

    async def receive_data(self, websocket):
        while True:
            message = await websocket.recv()
            price_symbol_data = await self.process_message(message)
            if price_symbol_data is not None:
                return price_symbol_data

    async def process_message(self, message):
        """Override this method in child classes to process received messages"""
        raise NotImplementedError
