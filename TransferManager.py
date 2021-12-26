import MongoAPI


def userCheckByID(userID: str, connection: MongoClient):
    return find("users", {"userID": userID}, connection)


def userCheckByName(username: str, connection: MongoClient):
    return find("users", {"username": username}, connection)


def transfer(userID: str, receiver: str, currencyID: str, amount: double, connection: MongoClient):
    sender = find("users", {"userID": userID}, connection)
    if userCheckByID(userID, connection):
        return -1  # Error, sender not found!
    if userCheckByName(receiver, connection):
        return -2  # Error, receiver not found!
    if sender.currencies[currencyID] < amount:
        return -3  # Error, sender does not have the required amount of the specified currency on his account balance.
    if sender.currencies[currencyID] == amount:
        print("Update not yet implemented.")
        # CRUD Update needed to remove specified currency from sender as their total is 0.
    else:
        print("Update not yet implemented.")
        # CRUD Update needed to reduce specified currency total by the amount sent.

    if receiver.currencies[currencyID]:
        print("Update not yet implemented.")
        # CRUD Update needed to add specified amount of currency to receiver's total.
    else:
        print("Update not yet implemented.")
        # CRUD Update needed to add specified currency to receiver's account balance.
