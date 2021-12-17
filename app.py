from flask import Flask, render_template, request, url_for
from ExchangeRateAPI import getExchangeRates
import json


app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


@app.route('/post', methods=['POST'])
def post():
    return render_template("POST.html")


@app.route('/rates')
def rates():
    r = getExchangeRates()
    rate = json.loads(r.content)
    r = json.dumps(rate, indent=4, sort_keys=True)
    return render_template("RATES.html", r=r)


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


if __name__ == '__main__':
    app.run(debug=True)
