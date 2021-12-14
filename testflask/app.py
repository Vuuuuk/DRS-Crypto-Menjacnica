from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


@app.route('/post', methods=['POST'])
def post():
    return render_template("POST.html")


@app.route('/param', methods=['POST'])
def param():
    t = request.form['text']
    return render_template("PARAM.html", t=t)


@app.route('/get', methods=['GET'])
def get():
    return render_template("GET.html")


if __name__ == '__main__':
    app.run(debug=True)
