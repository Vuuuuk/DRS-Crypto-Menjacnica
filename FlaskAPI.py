from flask import Flask, render_template, request, session, flash
from Engine import returnPopularCoins, returnFind, closeMongoConnection
from livereload import Server

app = Flask(__name__)
app.secret_key = "secretkey" #Eventualno premestiti u neki config/sakriti kljuc

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", popularCoins=returnPopularCoins(5))

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
            return render_template("index.html", popularCoins=returnPopularCoins(5))
        else:
            flash("Invalid username or password!", "info")

    return render_template("index.html", popularCoins=returnPopularCoins(5))

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("user_id", None)
    return render_template("index.html", popularCoins=returnPopularCoins(5))

@app.route("/notLoggedIn", methods=["GET"])
def notLoggedIn():
    flash("You have to be logged in!", "info")
    return render_template("index.html", popularCoins=returnPopularCoins(5))

#NOT IMPLEMENTED

@app.route("/transfer", methods=["POST"])
def transfer():
    flash("Account not verified!", "info") # Status transakcije prikazati ovde ili realizovati funkcionalnost na History stranici
    return render_template("index.html", popularCoins=returnPopularCoins(5))

#NOT IMPLEMENTED


# app.run(port=25565, debug=True)
server = Server(app.wsgi_app)
server.serve()

closeMongoConnection()
