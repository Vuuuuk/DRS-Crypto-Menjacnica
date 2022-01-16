from flask import Flask, render_template, request, session, flash
from Engine import *
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


@app.route("/register", methods=["POST"])
def register():
    firstName = request.form["register_firstname"]
    surname = request.form["register_surname"]
    address = request.form["register_address"]
    city = request.form["register_city"]
    state = request.form["register_state"]
    tel = request.form["register_tel"]
    email = request.form["register_email"]
    password = request.form["register_password"]
    user = returnFind("users", "email", email)
    if not user:
       User = {
           firstName :  firstName,
           surname :  surname,
           address :  address,
           city :  city,
           state :  state,
           tel :  tel,
           email :  email,
           password :  passwrod,
           AvailableCoind : {},
           IsVerified : false
       }
       insertUser(User)
    else:
        flash("This email already has an account!")

    return render_template("index.html", popularCoins=returnPopularCoins(5))

@app.route("/swap")
def swap:
    fromCoins = request.form["swap_userCoins"]
    toCoins = request.form["swap_availableCoins"]
    fromAmount = request.form["swap_userAmount"]
    toAmount = request.form["swap_availableAmount"]

    userMail = session["user_id"]

    User = returnFind("users", "Email", userMail)




@app.route("/modify", methods=["POST"])
def modify():
    firstName = request.form["account_firstname"]
    surname = request.form["account_surname"]
    address = request.form["account_address"]
    city = request.form["account_city"]
    state = request.form["account_state"]
    tel = request.form["account_tel"]
    email = request.form["account_email"]
    password = request.form["account_password"]
    user = returnFind("users", "email", email)
    if not user:
       User = {
           firstName :  firstName,
           surname :  surname,
           address :  address,
           city :  city,
           state :  state,
           tel :  tel,
           email :  email,
           password :  passwrod,
           AvailableCoind : {},
           IsVerified : false
       }
       updateUser(User)
    else:
        flash("This email already has an account!")

    return render_template("index.html", popularCoins=returnPopularCoins(5))


@app.route("/transfer", methods=["POST"])
def transfer():
    flash("Account not verified!", "info") # Status transakcije prikazati ovde ili realizovati funkcionalnost na History stranici
    return render_template("index.html", popularCoins=returnPopularCoins(5))

#NOT IMPLEMENTED


# app.run(port=25565, debug=True)
server = Server(app.wsgi_app)
server.serve()

closeMongoConnection()
