from flask import Flask, render_template, jsonify, request, session, flash
import json, requests, threading, time

app = Flask(__name__)
app.secret_key = "secretkey" #ANTI-COOKIE tampering, eventually has to be moved in a seperate file

#MARKET STATS AUTOMATIC UPDATE WITH A SINGLE DAEMON THREAD AND SOME AJAX

def coinDataRefresh():
    while True:
        coinDataRaw = requests.get("http://127.0.0.1:5001/coinCapAPI")
        if(coinDataRaw.ok):
            coinDataRefresh.coinData = json.loads(coinDataRaw.content)
            time.sleep(60)
        else:
            print("CoinCapAPI request failed with error -> ", coinDataRaw.status_code)

coinDataRefreshThread = threading.Thread(target=coinDataRefresh)
coinDataRefreshThread.setDaemon(True)
coinDataRefreshThread.start()

@app.route("/refreshMarketStatsLoggedIn", methods=["POST"])
def refreshLoggedIn():
    return jsonify("", render_template("refreshedMarketStatsLoggedIn.html", popularCoins=coinDataRefresh.coinData))

@app.route("/refreshMarketStatsNotLoggedIn", methods=["POST"])
def refreshNotLoggedIn():
    return jsonify("", render_template("refreshedMarketStatsNotLoggedIn.html", popularCoins=coinDataRefresh.coinData))

#MARKET STATS AUTOMATIC UPDATE WITH A SINGLE DAEMON THREAD AND SOME AJAX

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html",  popularCoins=coinDataRefresh.coinData)

@app.route("/login", methods=["POST"])
def login():
    session.pop("user_id", None)

    loginPayload = {"table": "users", "key": "Email", "searchParam": request.form["login_email"]}
    userLoginDataRaw = requests.get("http://0.0.0.0:5001/loginCheck", params=loginPayload)
    userLoginData = json.loads(userLoginDataRaw.content)

    if not userLoginData:
        flash("Invalid username or password!", "info")
    else:
        if userLoginData[0]["Password"] == userLoginData[0]["Password"]:
            session["user_id"] = userLoginData[0]["Email"]
            return render_template("index.html", popularCoins=coinDataRefresh.coinData)
        else:
            flash("Invalid username or password!", "info")

    return render_template("index.html", popularCoins=coinDataRefresh.coinData)

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("user_id", None)
    return render_template("index.html", popularCoins=coinDataRefresh.coinData)


@app.route("/notLoggedIn", methods=["GET"])
def notLoggedIn():
    flash("You have to be logged in!", "info")
    return render_template("index.html", popularCoins=coinDataRefresh.coinData)


@app.route("/transfer", methods=["POST"])
def transfer():
    flash("Account not verified!", "info") # Status transakcije prikazati ovde ili realizovati funkcionalnost na History stranici
    return render_template("index.html", popularCoins=coinDataRefresh.coinData)

    #NOT IMPLEMENTED

if __name__ == "__main__":
    app.run(port=5000, debug=True, host="0.0.0.0")

