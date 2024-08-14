# Prices API

A tool to retrieve real-time prices information from Binance and Kraken






## Deployment

To deploy this project run

```bash
  docker compose build

  docker compose up
```




## API Reference

#### retrieve prices
You can use Postman to test endpoint

```http
  GET /api/prices
```

| Parameters    | Type       | Description                |
| :--------     | :-------   | :------------------------- |
| `exchange`    | `string`   | 'Binance' or 'Kraken'      |
| `pair`        | `string`   | your desired cryptopair    |




