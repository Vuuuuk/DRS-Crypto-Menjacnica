from multiprocessing import Process

from CoinCapAPI import getAssetsCoinCapAPI
from MongoAPI import *
from flask import Flask, request

engineAPI = Flask(__name__)

client = connect("vuk_radunovic", "drs123")

@engineAPI.route("/coinCapAPI", methods=["GET"])
def returnpopularCoins():
    insertJSON("coinCapAPI", getAssetsCoinCapAPI(), client)
    filterJSON("coinCapAPI", client)
    return getPopularCoins("coinCapAPI", 5, client)

@engineAPI.route("/verifyUser", methods=["GET"])
def returnUserVerificationStatus():
    return verificationUpdate(request.args.get("table"), request.args.get("searchKey"), request.args.get("searchParam"), request.args.get("updateKey"), request.args.get("updateParam"), client)

@engineAPI.route("/findData", methods=["GET"])
def returnData():
    return find(request.args.get("table"), request.args.get("key"), request.args.get("searchParam"), client)

@engineAPI.route("/findAllData", methods=["GET"])
def returnAllData():
    return dispalyAll(request.args.get("table"), client)

@engineAPI.route("/transaction", methods=["GET"])
def transaction():
    # 0 - Kupovina, 1 - Exchange, 2 - Transfer
    p = Process(target=performTransaction, args=(request.args.get("user1"), request.args.get("user2"), request.args.get("currID"),
                                                 request.args.get("amount"), "dusan_radulovic", "drs123", request.args.get("transType"),
                                                 request.args.get("transCurr"), request.args.get("convVal"), ))
    p.daemon = True
    p.start()

@engineAPI.route("/userBalance", methods=["GET"])
def returnUserBalance():
    return getUserBalance(request.args.get("userMail"), client)

@engineAPI.route("/getAvailableCoins", methods=["GET"])
def returnAvailableCoins():
    return json.dumps(getAvailableCoins("coinCapAPI", client))

@engineAPI.route("/insertUser", methods=["POST"])
def insertUser():
    return insertuser("users", request.form["Email"], request.form, client)

@engineAPI.route("/updateUser", methods=["POST"])
def updateUser():
    return updateuser("users", request.form["Email"], request.form, client)

if __name__ == "__main__":
    engineAPI.run(port=5001, debug=True, host="0.0.0.0")
    client.close() #Nisam siguran da li mogu da ugasim konekciju ovako/na ovom mestu
