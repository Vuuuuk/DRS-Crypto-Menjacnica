import json

import requests


def getExchangeRates():
    url = 'https://rest.coinapi.io/v1/exchangerate/USD?invert=true'
    headers = {'X-CoinAPI-Key': 'E72E3DA0-51EB-42C1-9B66-00ADA4D114E3'}
    parsed = json.loads(requests.get(url, headers=headers).content)
    return json.dumps(parsed, indent=4, sort_keys=True)
