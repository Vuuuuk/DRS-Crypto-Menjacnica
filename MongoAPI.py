import pymongo
from pymongo import MongoClient

address = "77.105.59.252"
dataBase = "CryptoMenjacnica"

def connect(username : str, password : str):
    connectionString =  "mongodb://" \
                        "{username}:{password}@{address}:" \
                        "27017/?authSource={dataBase}"\
                        .format(username = username, password = password, address = address, dataBase = dataBase)
    return MongoClient(connectionString)

def createTable(tableName : str, client):
    db = client[dataBase]
    if tableName in db.list_collection_names():
        return print("Error -> " + tableName + " already exists.\n")
    else:
        client[dataBase].create_collection(tableName)
        return print("Success -> " + tableName + " successfully created.\n")

def dropTable(tableName : str, client):
    db = client[dataBase]
    if(tableName in db.list_collection_names()):
        db[tableName].drop()
        return print("Success -> " + tableName + " dropped successfully.\n")
    else:
        return print("Error -> " + tableName + " not found.\n")

def insert(tableName : str, key: str, data : dict, client):
    db = client[dataBase]
    if(tableName in db.list_collection_names()):
        table = db[tableName]
        if(table.find_one({key : data[key]})):
            return print("Error -> data already exists.\n")
        else:
            table.insert_one(data)
            return print("Success -> data inserted successfully.\n")
    else:
        return print("Error -> " + tableName + " not found.\n")

def insertJSON(tableName: str, data, client):
    db = client[dataBase]
    if(tableName in db.list_collection_names()):
        table = db[tableName]
        removeAll(tableName, client)
        table.insert_many(data["data"])
        return print("Success -> JSON inserted successfully.\n")
    else:
        return print("Error -> " + tableName + " not found.\n")

def filterJSON(tableName: str, client):
    db = client[dataBase]
    if(tableName in db.list_collection_names()):
        table = db[tableName]
        table.update_many({}, {"$unset": {"id": ""}})
        table.update_many({}, {"$unset": {"supply": ""}})
        table.update_many({}, {"$unset": {"maxSupply": ""}})
        table.update_many({}, {"$unset": {"marketCapUsd": ""}})
        table.update_many({}, {"$unset": {"volumeUsd24Hr": ""}})
        table.update_many({}, {"$unset": {"changePercent24Hr": ""}})
        table.update_many({}, {"$unset": {"vwap24Hr": ""}})
        table.update_many({}, {"$unset": {"explorer": ""}})
        return print("Success -> " + tableName + " filtered successfully.\n")
    else:
        return print("Error -> " + tableName + " not found.\n")

def remove(tableName: str, keyParam: str, searchParam: str, client):
    db = client[dataBase]
    if(tableName in db.list_collection_names()):
        table = db[tableName]
        if(table.find_one({keyParam: searchParam})):
            table.delete_one({keyParam: searchParam})
            return print("Success -> data deleted.\n")
        else:
            return print("Error -> data does not exist.\n")
    else:
        return print("Error -> " + tableName + " not found.\n")

def delete(tableName: str, keyParam: str, searchParam: str, deleteParam: str, client):
    db = client[dataBase]
    if(tableName in db.list_collection_names()):
        table = db[tableName]
        if(table.find_one({keyParam: searchParam})):
            table.update_one({keyParam: searchParam}, {"$set": {deleteParam: 0.0}})
            return print("Success -> data deleted.\n")
        else:
            return print("Error -> data does not exist.\n")
    else:
        return print("Error -> " + tableName + " not found.\n")

def removeAll(tableName: str, client):
    db = client[dataBase]
    if(tableName in db.list_collection_names()):
        table = db[tableName]
        table.delete_many({})
        return print("Success -> table deleted.\n")
    else:
        return print("Error -> " + tableName + " not found.\n")

def find(tableName : str, key: str, searchParam : str, client):
    db = client[dataBase]
    if(tableName in db.list_collection_names()):
        table = db[tableName]
        return list(table.find({key: searchParam}))
    else:
        return print("Error -> " + tableName + " not found.\n")

def dispalyAll(tableName : str, client):
    db = client[dataBase]
    if(tableName in db.list_collection_names()):
        table = db[tableName]
        return list(table.find())
    else:
        return print("Error -> " + tableName + " not found.\n")

def update(tableName : str, searchParam : str, updateParam : str, client):
    db = client[dataBase]
    if(tableName in db.list_collection_names()):
        table = db[tableName]
        table.update_many({"name": searchParam}, {"$set": {"name": updateParam}})
        return print("Success -> data updated.\n")
    else:
        return print("Error -> " + tableName + " not found.\n")

########################################################################################################################

def getPopularCoins(tableName: str, numOfCoins: int, client):
    db = client[dataBase]
    if(tableName in db.list_collection_names()):
        table = db[tableName]
        return list(table.find({}, {"_id": 0, "rank": 0}).limit(numOfCoins))
    else:
        return print("Error -> " + tableName + " not found.\n")