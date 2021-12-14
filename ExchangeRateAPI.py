import requests


def getExchangeRates():
    url = 'https://rest.coinapi.io/v1/exchangerate/USD?invert=true'
    headers = {'X-CoinAPI-Key': 'E72E3DA0-51EB-42C1-9B66-00ADA4D114E3'}
    return requests.get(url, headers=headers)
