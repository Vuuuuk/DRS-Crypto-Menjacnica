from CoinCapAPI import getAssetsCoinCapAPI
from MongoAPI import *

client = connect("vuk_radunovic", "drs123")
filterJSON("coinCapAPI", client)
#validCard = {"Number": "4242 4242 4242 4242", "Date": "02/23", "CVC": "123"}
#insert("ccards", "Number", validCard, client)


def returnPopularCoins(numOfCoins: int):
    return getPopularCoins("coinCapAPI", numOfCoins, client)

def returnAllCoins():
    return getAllCoins("coinCapAPI", client)

def returnFind(tableName: str, key: str, searchParam: str):
    return find(tableName, key, searchParam, client)

def returnFindAll(tableName: str):
    return dispalyAll(tableName, client)

def returnUpdateVerify(tableName : str, searchKey:str, searchParam : str, updateKey:str, updateParam : bool):
    return updateVerify(tableName, searchKey, searchParam, updateKey, updateParam, client)

def closeMongoConnection():
    client.close()





