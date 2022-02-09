from flask import Flask, render_template, request, session, flash
from Engine import returnPopularCoins, returnFind, closeMongoConnection, returnAllCoins, returnFindAll, updateElement
from livereload import Server

app = Flask(__name__)
app.secret_key = "secretkey" #Eventualno premestiti u neki config/sakriti kljuc

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", popularCoins=returnPopularCoins(5),transactionHistory=returnFindAll("transactions"))

@app.route("/login", methods=["POST"])
def login():
    session.pop("user_id", None)

    email = request.form["login_email"]
    password = request.form["login_password"]

    user = returnFind("users", "Email", email)
    if not user:
        flash("Invalid username or password!", "info")
    else:
        if user[0]["Password"] == password:
            session["user_id"] = user[0]["Email"]  # Proveriti kako je moguce vezati na _ID
            return render_template("index.html", popularCoins=returnPopularCoins(5),transactionHistory=returnFindAll("transactions"))
        else:
            flash("Invalid username or password!", "info")

    return render_template("index.html", popularCoins=returnPopularCoins(5), transactionHistory=returnFindAll("transactions"))

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("user_id", None)
    return render_template("index.html", popularCoins=returnPopularCoins(5),transactionHistory=returnFindAll("transactions"))

@app.route("/notLoggedIn", methods=["GET"])
def notLoggedIn():
    flash("You have to be logged in!", "info")
    return render_template("index.html", popularCoins=returnPopularCoins(5),transactionHistory=returnFindAll("transactions"))
@app.route("/transfer", methods=["POST"])
def transfer():
    flash("Account not verified!", "info") # Status transakcije prikazati ovde ili realizovati funkcionalnost na History stranici
    return render_template("index.html", popularCoins=returnPopularCoins(5), transactionHistory=returnFindAll("transactions"))
@app.route("/verifyUser", methods=["POST"])
def verify():
    number = request.form["verify_creditcard"]
    name = request.form["verify_name"]
    date = request.form["verify_date"]
    cvc = request.form["verify_cvc"]

    card = returnFind("ccards", "Number", str(number))
    user = returnFind("users", "Email", session["user_id"])
    if not card:
        flash("Unable to verify! Invalid card number!", "info")
    else:
        if name == user[0]["FirstName"] and card[0]["Date"] == str(date) and card[0]["CVC"] == str(cvc):
            updateElement("users", "IsVerified", "true")
            return render_template("index.html", popularCoins=returnPopularCoins(5), transactionHistory=returnFindAll("transactions"))
        else:
            flash("Unable to verify! Invalid card parameters!", "info")

    return render_template("index.html", popularCoins=returnPopularCoins(5), transactionHistory=returnFindAll("transactions"))

# app.run(port=25565, debug=True)
server = Server(app.wsgi_app)
server.serve()

closeMongoConnection()
