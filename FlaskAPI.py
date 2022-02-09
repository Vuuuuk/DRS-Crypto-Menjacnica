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
    firsttName = request.form["register_firstname"]
    surname = request.form["register_surname"]
    address = request.form["register_address"]
    city = request.form["register_city"]
    state = request.form["register_state"]
    tel = request.form["register_tel"]
    email = request.form["register_email"]
    password = request.form["register_password"]
    user = returnFind("users", "email", email)
    AvailableCoins = {}
    if not user:
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
       insertUser(User)
    else:
        flash("This email already has an account!")

    return render_template("index.html", popularCoins=returnPopularCoins(5))

@app.route("/swap")
def swap():
    fromCoins = request.form["swap_userCoins"]
    toCoins = request.form["swap_availableCoins"]
    fromAmount = request.form["swap_userAmount"]
    toAmount = request.form["swap_availableAmount"]

    userMail = session["user_id"]

    User = returnFind("users", "Email", userMail)

    coin1 = getcoin(fromCoins)
    coin2 = getcoin(toCoins)

    if User["AvailableCoins"][coin1] < fromAmount:
        flash("You don't have enough coins")
        return render_template("index.html", popularCoins=returnPopularCoins(5))

    if not User["AvailableCoins"][coin2]:
        User["AvailableCoins"][coin2] = toAmount
    else:
        User["AvailableCoins"][coin2] += toAmount
    User["AvailableCoins"][coin1] -= fromAmount

    updateUser(User)

    return render_template("index.html", popularCoins=returnPopularCoins(5))


@app.route("/modify", methods=["POST"])
def modify():
    firstName = request.form["account_firstname"]
    surname = request.form["account_surname"]
    address = request.form["account_address"]
    city = request.form["account_city"]
    state = request.form["account_state"]
    tel = request.form["account_tel"]
    email = request.form["account_email"]
    user = returnFind("users", "Email", email)
    if not user:
        flash("Something went wrong")
        return render_template("index.html", popularCoins=returnPopularCoins(5))

    User = {
       "FirstName" :  firstName,
       "LastName" :  surname,
       "Address" :  address,
       "City" :  city,
       "State" :  state,
       "PhoneNumber" :  tel,
       "Email" :  email,
       "Password" :  user[0]["Password"],
       "AvailableCoind" : user[0]["AvailableCoins"],
       "IsVerified" : user[0]["IsVerified"]
       }
    updateUser(User)

    return render_template("index.html", popularCoins=returnPopularCoins(5))





@app.route("/transfer", methods=["POST"])
def transfer():
    toMail = request.form["recipients_email"]
    toAmount = request.form["recipients_amount"]
    fromCoin = request.form["senders_available_coins"]
    fromMail = session["user_id"]

    user = returnFind("users", "Email", fromMail)
    if not user["AvailableCoins"][fromCoin]:
        flash("You don't have that coin","info")
    if user["AvailableCoins"][fromCoin] < toAmount:
        flash("You don't have that much coin")
    else :
        toUser = returnFind("users", "Email", toMail)
        if not toUser["AvailableCoins"][fromCoin]:
            toUser["AvailableCoins"][fromCoin] = toAmount
        else :
            toUser["AvailableCoins"][fromCoin] += toAmount
        updateUser(toUser)
        user["AvailableCoins"][fromCoin] -= toAmount
        updateUser(user)


    return render_template("index.html", popularCoins=returnPopularCoins(5))

#NOT IMPLEMENTED


# app.run(port=25565, debug=True)
server = Server(app.wsgi_app)
server.serve()

closeMongoConnection()
