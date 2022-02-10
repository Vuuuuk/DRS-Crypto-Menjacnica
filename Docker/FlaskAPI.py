from flask import Flask, render_template, jsonify, request, session, flash
import json, requests, threading, time

app = Flask(__name__)
app.secret_key = "secretkey" #ANTI-COOKIE tampering, eventually has to be moved in a seperate file
ipval = "http://engine:5001/"
transactionPayload = {"table": "transactions"}

#MARKET STATS AUTOMATIC UPDATE WITH A SINGLE DAEMON THREAD AND SOME AJAX

def dataRefresh():
    while True:
        coinDataRaw = requests.get("http://engine:5001/coinCapAPI")
        transactionDataRaw = requests.get("http://engine:5001/findAllData", params=transactionPayload)

        if(coinDataRaw.ok):
            dataRefresh.coinData = json.loads(coinDataRaw.content)
        else:
            print("CoinCapAPI request failed with error -> ", coinDataRaw.status_code)
        if(transactionDataRaw.ok):
            dataRefresh.transactionData = json.loads(transactionDataRaw.content)
        else:
            print("Transaction history refresh request failed with error -> ", transactionDataRaw.status_code)

        time.sleep(60)

coinDataRefreshThread = threading.Thread(target=dataRefresh)
coinDataRefreshThread.daemon = True
coinDataRefreshThread.start()

@app.route("/refreshMarketStatsLoggedIn", methods=["POST"])
def refreshLoggedIn():
    return jsonify("", render_template("refreshedMarketStatsLoggedIn.html", popularCoins=dataRefresh.coinData))

@app.route("/refreshMarketStatsNotLoggedIn", methods=["POST"])
def refreshNotLoggedIn():
    return jsonify("", render_template("refreshedMarketStatsNotLoggedIn.html", popularCoins=dataRefresh.coinData))

@app.route("/refreshTransactionHistory", methods=["POST"])
def refreshTransactionHistory():
    return jsonify("", render_template("refreshedTransactionHistory.html", transactionHistory=dataRefresh.transactionData))

#MARKET STATS AUTOMATIC UPDATE WITH A SINGLE DAEMON THREAD AND SOME AJAX

@app.route("/", methods=["GET"])
def index():
    if "user_id" in session:
        if request.args.get("buy_availableCoins"):
            parameters = dict(request.args)
            if float(parameters["buy_availableCoins"].split("/")[1]) * float(parameters["buy_userAmount"]) == float(
                    parameters["buy_calculatedPrice"]):
                requests.get(ipval + "/transaction?user1=" + session["user_id"] + "&user2=Menjacnica&currID=USD&amount="
                             + parameters["buy_calculatedPrice"] + "&transType=0&transCurr="
                             + parameters["buy_availableCoins"].split("/")[0] + "&convVal=" + parameters["buy_userAmount"])

        balanceJson = requests.get(ipval + "userBalance?userMail=" + session["user_id"])
        try:
            bal = json.loads(balanceJson.content)
        except:
            bal = {}
        coinsJson = requests.get(ipval + "/getAvailableCoins")
        try:
            coins = json.loads(coinsJson.content)
        except:
            coins = {}

        return render_template("index.html", popularCoins=dataRefresh.coinData, userBalance=bal, availableCoins=coins, transactionHistory=dataRefresh.transactionData)

    return render_template("index.html",  popularCoins=dataRefresh.coinData)

@app.route("/login", methods=["POST"])
def login():
    session.pop("user_id", None)

    loginPayload = {"table": "users", "key": "Email", "searchParam": request.form["login_email"]}
    userLoginDataRaw = requests.get(ipval + "findData", params=loginPayload)
    userLoginData = json.loads(userLoginDataRaw.content)

    if not userLoginData:
        flash("Invalid username or password!", "info")
    else:
        if userLoginData[0]["Password"] == userLoginData[0]["Password"]:
            balanceJson = requests.get(ipval + "userBalance?userMail=" + userLoginData[0]["Email"])
            try:
                bal = json.loads(balanceJson.content)
            except:
                bal = {}
            coinsJson = requests.get(ipval + "/getAvailableCoins")
            try:
                coins = json.loads(coinsJson.content)
            except:
                coins = {}
            session["user_id"] = userLoginData[0]["Email"]
            return render_template("index.html", popularCoins=dataRefresh.coinData, userBalance=bal, availableCoins=coins, transactionHistory=dataRefresh.transactionData)
        else:
            flash("Invalid username or password!", "info")

    return render_template("index.html", popularCoins=dataRefresh.coinData)

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("user_id", None)
    return render_template("index.html", popularCoins=dataRefresh.coinData)


@app.route("/notLoggedIn", methods=["GET"])
def notLoggedIn():
    flash("You have to be logged in!", "info")
    return render_template("index.html", popularCoins=dataRefresh.coinData)


@app.route("/register", methods=["POST"])
def register():
    firsttName = request.form["register_firstname"]
    surname = request.form["register_surname"]
    address = request.form["register_address"]
    city = request.form["register_city"]
    state = request.form["register_state"]
    tel = request.form["register_tel"]
    email = request.form["register_email"]
    password = request.form["register_password"]
    user = requests.get(ipval + "userBalance?userMail=" + email)
    if user.content:
       User = {
           "FirstName" :  firsttName,
           "LastName" :  surname,
           "Address" :  address,
           "City" :  city,
           "State" :  state,
           "PhoneNumber" :  tel,
           "Email" :  email,
           "Password" :  password,
           "AvailableCoins" : {},
           "IsVerified" : False
       }
       requests.post(ipval + "insertUser", User)
    else:
        flash("This email already has an account!")

    return render_template("index.html", popularCoins=dataRefresh.coinData)

@app.route("/swap", methods=["POST"])
def swap():

    fromCoins = request.form["swap_userCoins"]
    toCoins = request.form["swap_availableCoins"]
    fromAmount = request.form["swap_userAmount"]
    toAmount = request.form["swap_availableAmount"]

    requests.get(ipval + "/transaction?user1=" + session["user_id"] + "&user2=Menjacnica&currID=" + fromCoins + "&amount="
                 + fromAmount + "&transType=1&transCurr=" + toCoins + "&convVal=" + toAmount)

    return render_template("index.html", popularCoins=dataRefresh.coinData, transactionHistory=dataRefresh.transactionData)


@app.route("/modify", methods=["POST"])
def modify():
    firstName = request.form["account_firstname"]
    surname = request.form["account_surname"]
    address = request.form["account_address"]
    city = request.form["account_city"]
    state = request.form["account_state"]
    tel = request.form["account_tel"]
    email = session["user_id"]
    user = requests.get(ipval + "userBalance?userMail=" + email)
    if not user.content:
        flash("Something went wrong please try again!")
        return render_template("index.html", popularCoins=dataRefresh.coinData, transactionHistory=dataRefresh.transactionData)

    User = {
       "FirstName" :  firstName,
       "LastName" :  surname,
       "Address" :  address,
       "City" :  city,
       "State" :  state,
       "PhoneNumber" :  tel,
       "Email" :  email
       }

    requests.post(ipval + "updateUser", User)

    return render_template("index.html", popularCoins=dataRefresh.coinData, transactionHistory=dataRefresh.transactionData)

@app.route("/transfer", methods=["POST"])
def transfer():
    toMail = request.form["recipients_email"]
    toAmount = request.form["recipients_amount"]
    fromCoin = request.form["senders_available_coins"]

    requests.get(
        ipval + "/transaction?user1=" + session["user_id"] + "&user2=" + toMail + "&currID=" + fromCoin + "&amount="
        + toAmount + "&transType=2&transCurr=&convVal=")

    return render_template("index.html", popularCoins=dataRefresh.coinData, transactionHistory=dataRefresh.transactionData)

@app.route("/verifyUser", methods=["POST"])
def verify():
    transactionPayload = {"table": "transactions"}
    transactionDataRaw = requests.get("http://engine:5001/findAllData", params=transactionPayload)
    transactionData = json.loads(transactionDataRaw.content)

    creditCardPayload = {"table": "ccards", "key": "Number", "searchParam": request.form["verify_creditcard"]}
    creditCardDataRaw = requests.get("http://engine:5001/findData", params=creditCardPayload)
    creditCardData = json.loads(creditCardDataRaw.content)

    userPayload = {"table": "users", "key": "Email", "searchParam": session["user_id"]}
    userDataRaw = requests.get("http://engine:5001/findData", params=userPayload)
    userData = json.loads(userDataRaw.content)

    if not creditCardData:
        flash("Unable to verify invalid card number!", "info")
    else:
        if request.form["verify_name"] == userData[0]["FirstName"] and creditCardData[0]["Date"] == str(request.form["verify_date"]) and creditCardData[0]["CVC"] == str(request.form["verify_cvc"]):
            if(userData[0]["IsVerified"]):
                flash("You are already verified!", "info")
            else:
                updatePayload = {"table": "users", "searchKey": "FirstName", "searchParam": userData[0]["FirstName"], "updateKey": "IsVerified", "updateParam": True}
                requests.get("http://engine:5001/verifyUser", params=updatePayload)
                return render_template("index.html", popularCoins=dataRefresh.coinData, transactionHistory=dataRefresh.transactionData)
        else:
            flash("Unable to verify invalid card parameters!", "info")

    return render_template("index.html", popularCoins=dataRefresh.coinData, transactionHistory=dataRefresh.transactionData)

if __name__ == "__main__":
    app.run(port=5000, debug=True, host="0.0.0.0")

