import json

from ExchangeRateAPI import getExchangeRates

exchangeRateJSON = getExchangeRates()
parsed = json.loads(exchangeRateJSON.content)
print(json.dumps(parsed, indent=4, sort_keys=True))