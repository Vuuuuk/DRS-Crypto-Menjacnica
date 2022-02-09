import json
import random
from time import sleep

from pymongo import MongoClient
from Cryptodome.Hash import keccak

address = "79.175.70.227"
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
        return json.dumps(list(table.find({key: searchParam}, {"_id": 0})))
    else:
        return print("Error -> " + tableName + " not found.\n")

def dispalyAll(tableName : str, client):
    db = client[dataBase]
    if(tableName in db.list_collection_names()):
        table = db[tableName]
        return json.dumps(list(table.find({}, {"_id": 0})))
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
        return json.dumps(list(table.find({}, {"_id": 0, "rank": 0}).limit(numOfCoins)))
    else:
        return print("Error -> " + tableName + " not found.\n")


def getCoin(tableName: str, coin: str, client):
    db = client[dataBase]
    if tableName in db.list_collection_names():
        table = db[tableName]
        found = list(table.find({"symbol": coin}, {"_id": 0, "rank": 0}))
        return found[0]
    else:
        return print("Error -> " + tableName + " not found.\n")


def getUserBalance(userMail: str, client):
    db = client[dataBase]
    if "users" in db.list_collection_names():
        table = db["users"]
        userCoins = list(table.find({"Email": userMail}, {"_id": 0}))
        coins = list()
        for coin in userCoins[0]["AvailableCoins"]:
            if coin == "USD":
                continue
            temp = getCoin("coinCapAPI", coin, client)
            temp["balance"] = userCoins[0]["AvailableCoins"][coin]
            coins.append(temp)
        return json.dumps(coins)
    else:
        return print("Error -> failed finding user.\n")


def getAvailableCoins(tableName: str, client):
    db = client[dataBase]
    if(tableName in db.list_collection_names()):
        table = db[tableName]
        return list(table.find({}, {"_id": 0, "rank": 0}))
    else:
        return print("Error -> " + tableName + " not found.\n")

def updateBalance(tableName : str, searchKey: str, searchParam : str, updateKey: str, updateParam : str, client):
    db = client[dataBase]
    if(tableName in db.list_collection_names()):
        table = db[tableName]
        userCoins = list(table.find({"Email": searchParam}, {"_id": 0}))[0]["AvailableCoins"]
        if userCoins.get(updateKey):
            userCoins[updateKey] += float(updateParam)
        else:
            userCoins[updateKey] = float(updateParam)
        table.update_many({searchKey: searchParam}, {"$set": {"AvailableCoins": userCoins}})
        return print("Success -> data updated.\n")
    else:
        return print("Error -> " + tableName + " not found.\n")

def verificationUpdate(tableName : str, searchKey: str, searchParam : str, updateKey: str, updateParam : bool, client):
    db = client[dataBase]
    if(tableName in db.list_collection_names()):
        table = db[tableName]
        table.update_many({searchKey: searchParam}, {"$set": {updateKey: bool(updateParam)}})
        return print("Success -> user verified.\n")
    else:
        return print("Error -> " + tableName + " not found.\n")

def performTransaction(user1: str, user2: str, currID: str, amount: float, username: str, password: str,
                       transType: int, transCurr: str, transVal: str):
    client = connect(username, password)
    db = client[dataBase]
    table = db["transactions"]
    userTable = db["users"]
    user1get = list(userTable.find({"Email": user1}, {"_id": 0}))[0]
    if user2 != "Menjacnica":
        user2get = list(userTable.find({"Email": user2}, {"_id": 0}))[0]
    else:
        user2get = "Menjacnica"
    transaction = dict()
    transaction["user1"] = user1
    transaction["user2"] = user2
    transaction["currID"] = currID
    transaction["amount"] = float(amount) * 1.05
    user1trans = json.loads(find("transactions", "user1", user1, client))
    print(user1trans)
    transID = len(user1trans)
    print(transID)
    transaction["userTransactionID"] = transID
    transaction["status"] = "U obradi"
    table.insert_one(transaction)

    if user1get and user2get and currID == "USD" or user1get["AvailableCoins"][currID] >= (float(amount) * 1.05):
        k = keccak.new(digest_bits=256)
        rand = random.Random()
        k.update(user1.encode())
        k.update(user2.encode())
        k.update(currID.encode())
        k.update(str(float(amount) * 1.05).encode())
        k.update(str(rand.randint(0, 10000)).encode())
        hashResult = k.hexdigest()
        sleep(5)
        table.update_one({"user1": user1, "userTransactionID": transID}, {"$set": {"status": "Obradjeno",
                                                                                   "hash": hashResult}})
        if transType == "0":
            print(transCurr)
            print(transVal)
            print(user1)
            updateBalance("users", "Email", user1, transCurr, transVal, client)
        if transType == "1":
            swap(user1, client, currID, transCurr, amount * 1.05, float(transVal))
        if transType == "2":
            transfer(currID, user1, amount, user2, client)
        client.close()
        return

    table.update_one({"user1": user1, "userTransactionID": transID}, {"$set": {"status": "Odbijeno"}})
    print("Error during transaction")
    client.close()

def insertuser(tableName : str, key: str, user, client):
    User = {
        "FirstName": user["FirstName"],
        "LastName": user["LastName"],
        "Address": user["Address"],
        "City": user["City"],
        "State": user["State"],
        "PhoneNumber": user["PhoneNumber"],
        "Email": user["Email"],
        "Password": user["Password"],
        "AvailableCoins": {},
        "IsVerified": False
    }

    db = client[dataBase]
    if(tableName in db.list_collection_names()):
        table = db[tableName]
        if(table.find_one({"Email" : key})):
            return print("Error -> data already exists.\n")
        else:
            table.insert_one(User)
            return print("Success -> data inserted successfully.\n")
    else:
        return print("Error -> " + tableName + " not found.\n")

def updateuser(tableName: str, searchParam: str, updateParam, client):
    User = {
        "FirstName": updateParam["FirstName"],
        "LastName": updateParam["LastName"],
        "Address": updateParam["Address"],
        "City": updateParam["City"],
        "State": updateParam["State"],
        "PhoneNumber": updateParam["PhoneNumber"],
        "Email": updateParam["Email"],
        "IsVerified": False
    }
    db = client[dataBase]
    if tableName in db.list_collection_names():
        table = db[tableName]
        table.find_one_and_replace({"Email": searchParam}, User)
        return print("Success -> data updated.\n")
    else:
        return print("Error -> " + tableName + " not found.\n")

def updateuser2(tableName: str, searchParam: str, updateParam, client):
        db = client[dataBase]
        if tableName in db.list_collection_names():
            table = db[tableName]
            table.find_one_and_replace({"Email": searchParam}, updateParam)
            return print("Success -> data updated.\n")
        else:
            return print("Error -> " + tableName + " not found.\n")


def swap(userMail, client, coin1: str, coin2: str, val1: float, val2: float):
    User = json.loads(find("users", "Email", userMail, client))[0]
    if coin2 in User["AvailableCoins"]:
        User["AvailableCoins"][coin2] += val1
    else:
        User["AvailableCoins"][coin2] = val1
    User["AvailableCoins"][coin1] -= val2

    updateuser2("users", User["Email"], User, client)

def transfer(coin1: str, fromMail, amount, toMail, client):
    user = json.loads(find("users", "Email", fromMail, client))[0]
    if coin1 not in user["AvailableCoins"]:
        print("No coin")
        return
    if float(user["AvailableCoins"][coin1]) < float(amount):
        print("Not enough coin")
        return
    else:
        toUser = json.loads(find("users", "Email", toMail, client))[0]
        if coin1 not in toUser["AvailableCoins"]:
            toUser["AvailableCoins"][coin1] = float(amount)
        else:
            toUser["AvailableCoins"][coin1] += float(amount)
        updateuser2("users", toMail, toUser, client)
        user["AvailableCoins"][coin1] -= float(amount) * 1.05
        updateuser2("users", fromMail, user, client)