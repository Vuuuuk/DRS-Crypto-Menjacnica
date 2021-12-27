from CoinCapAPI import getAssetsCoinCapAPI
from MongoAPI import *

client = connect("vuk_radunovic", "drs123")

def returnPopularCoins(numOfCoins: int):
    return getPopularCoins("coinCapAPI", numOfCoins, client)

def returnFind(tableName: str, key: str, searchParam: str):
    return find(tableName, key, searchParam, client)

def closeMongoConnection():
    client.close()





