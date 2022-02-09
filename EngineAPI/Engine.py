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

if __name__ == "__main__":
    engineAPI.run(port=5001, debug=True, host="0.0.0.0")
    client.close() #Nisam siguran da li mogu da ugasim konekciju ovako/na ovom mestu





