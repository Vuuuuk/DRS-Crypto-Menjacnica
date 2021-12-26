from pymongo import MongoClient

address = "77.105.56.166"
database = "CryptoMenjacnica"


def connect(username: str, password: str):
    connectionString = "mongodb://" \
                       "{username}:{password}@{address}:" \
                       "27017/?authSource={database}"\
                        .format(username=username, password=password, address=address, database=database)
    return MongoClient(connectionString)


def createTable(tableName: str, client):
    db = client[dataBase]
    if tableName in db.list_collection_names():
        return print("Error -> " + tableName + " already exists.\n")
    else:
        client[dataBase].create_collection(tableName)
        return print("Success -> " + tableName + " successfully created.\n")


def dropTable(tableName: str, client):
    db = client[dataBase]
    if tableName in db.list_collection_names():
        db[tableName].drop()
        return print("Success -> " + tableName + " dropped successfully.\n")
    else:
        return print("Error -> " + tableName + " not found.\n")


def insert(tableName: str, data: dict, client):
    db = client[dataBase]
    if tableName in db.list_collection_names():
        table = db[tableName]
        if table.find_one({"name": data["name"]}):
            return print("Error -> data already exists.\n")
        else:
            table.insert_one(data)
            return print("Success -> data inserted successfully.\n")
    else:
        return print("Error -> " + tableName + " not found.\n")


def remove(tableName: str, key: str, client):
    db = client[dataBase]
    if tableName in db.list_collection_names():
        table = db[tableName]
        if table.find_one({"name": key}):
            table.delete_one({"name": key})
            return print("Success -> data deleted.\n")
        else:
            return print("Error -> data does not exist.\n")
    else:
        return print("Error -> " + tableName + " not found.\n")


def find(tableName: str, searchParam: str, client):
    db = client[dataBase]
    if tableName in db.list_collection_names():
        table = db[tableName]
        return list(table.find({}, {searchParam: 1}))
    else:
        return print("Error -> " + tableName + " not found.\n")
