from flask import Flask, render_template, request, session, redirect, url_for
import os
import utils

app = Flask(__name__)
app.secret_key = os.urandom(32)

users = {"userNow": "userNowPass"}

@app.route("/", methods = ["GET", "POST"])
def root():
    if(session.has_key("username")):
        return render_template("home.html")
    else:
        return render_template("login.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    #person is currently logged in
    if(session.has_key("username")):
        return render_template("home.html")

    #if the participant has just logged in
    userNow = request.form["username"]
    userNowPass = request.form["password"]
    #if the account and such match
    if(userNow in users.keys()) and (users[userNow] == userNowPass):
        session["username"] = userNow
        return render_template("home.html")
    #if password is incorrect
    elif(userNow in users.keys()):
        flash("Wrong password")
        return render_template("login.html")
    elif(request.form["registerButton"] == "Register"):
        return render_template("signup.html")
    #if account does not exist
    else:
        flash("Press Register to create a new account, boy")
        return render_template("login.html")

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    newUser = request.form["newUser"]
    newPass = request.form["newPass"]
    if(newUser in users.keys()):
        flash("Bad, this account exist")
        return render_template("signup.html")
    else:
        session["username"] = newUser
        users[newUser] = newPass
        return render_template("home.html")
    
if __name__ == "__main__":
    app.debug = True
    app.run()
    
