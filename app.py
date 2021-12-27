from flask import Flask, render_template, request
from ExchangeRateAPI import getExchangeRates
from MongoAPI import connect, insert, createTable, dropTable, find, remove
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
    ret = find('coinCapAPI', username, client);

    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)
