import json

from django.http import JsonResponse
from prices.utils import get_prices


async def prices_view(request):
    if request.method == 'GET':
        try:
            data = json.loads(request.body)
            pair = data.get('pair') or None
            exchange = data.get('exchange') or None
            if exchange is not None:
                exchange = exchange.lower()
        except json.JSONDecodeError as e:
            print(e)
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        data = await get_prices(pair, exchange)
        data = json.dumps(data)
        return JsonResponse(data, safe=False)
