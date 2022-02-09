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

@engineAPI.route("/loginCheck", methods=["GET"]) #Moguce je koristiti i POST metodu, radi jednostavnije testiranja i prelaza ostavio sam ipak GET
def returnLoginData():
    return find(request.args.get("table"), request.args.get("key"), request.args.get("searchParam"), client)

if __name__ == "__main__":
    engineAPI.run(port=5001, debug=True)
    client.close() #Nisam siguran da li mogu da ugasim konekciju ovako/na ovom mestu





