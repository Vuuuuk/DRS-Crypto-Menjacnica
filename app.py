from flask import Flask, render_template, request
from ExchangeRateAPI import getExchangeRates
from MongoAPI import connect, insert, createTable, dropTable, find, remove
import pymongo
import json


app = Flask(__name__)


client = connect("karlo_pest", "drs123")


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


@app.route('/post', methods=['POST'])
def post():
    return render_template("POST.html")


@app.route('/rates')
def rates():
    r = find("users", "admin", client)
    return render_template("RATES.html", r=r.index(1))


@app.route("/extend")
def extend():
    return render_template("extend1.html")


@app.route("/extend2")
def extends2():
    return render_template("extends2.html")


@app.route('/param', methods=['POST'])
def param():
    t = request.form['text']
    return render_template("PARAM.html", t=t)


@app.route('/get', methods=['GET'])
def get():
    return render_template("GET.html")


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    passw = request.form['pass']
    db = client["CryptoMenjacnica"]
    table = db["users"]
    user = table.find_one({"Username": username, "Password": passw})
    if  not user:
        return render_template("login.html", t="NO SUCH USER")
    text = "Welcome { }"
    return render_template("login.html", t = text.format(user["Username"]))


@app.route('/exchange')
def exchange():
    startCoin = request.form['startCoin']
    startCoinType = request.form['startCoinType']
    endCoinType = request.form['endCoinType']
    db = client["CryptoMenjacnica"]
    table = db["coinCapAPI"]
    startCoin = table.find({"symbol": startCoinType})
    endCoin = table.find({"symbol": endCoinType})

    endCoinNum = startCoin["priceUsd"] / endCoin["priceUsd"]

    #put this into the database





@app.route('/reg', methods=['POST'])
def reg():
    username = request.form['username']
    passw = request.form['pass']
    Firstname = request.form['fname']
    Lasttname = request.form['lname']
    db = client["CryptoMenjacnica"]
    table = db["users"]
    if table.count_documents({"Username": username}) == 0:
        return render_template("login.html", t="THAT USERNAME IS TAKEN")

    user = {
        "_id" : "ldkjsakfjbsk",
        "Username" : username,
        "Password" : passw,
        "FirstName" : Firstname,
        "LastName" : Lasttname

    }

    table.insert_one(user)

    return render_template("login.html", t= "Registration Complete")


@app.route('/modify', methods=['POST'])
def modify():
    username = request.form['username']
    passw = request.form['pass']
    Firstname = request.form['fname']
    Lasttname = request.form['lname']
    db = client["CryptoMenjacnica"]
    table = db["users"]
    if table.count_documents({"Username": username}) != 0:
        return render_template("login.html", t="THAT USERNAME DOES NOT EXIST")

    user = {
        "_id": "ldkjsakfjbsk",
        "Username": username,
        "Password": passw,
        "FirstName": Firstname,
        "LastName": Lasttname

    }

    table.find_one_and_replace({"Username" : username}, {user})
    return render_template("login.html", t="THAT USERNAME DOES NOT EXIST")




if __name__ == '__main__':
    app.run(debug=True)
