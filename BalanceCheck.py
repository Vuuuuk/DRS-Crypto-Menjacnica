import MongoAPI


def USDTotal(userID: str, connection: MongoClient):
    user = find("users", {"userID": userID}, connection)
    currencies = user.currencies
    result = 0.0
    for currency in currencies:
        conversionRate = find("currencies", {"currencyID": currency["ID"]}, connection)["conversionRate"]
        result += currency["amount"] * conversionRate

    return result
