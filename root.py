from flask import Flask, render_template, request, session, redirect, url_for, flask
import os
import utils

app = Flask(__name__)
app.secret_key = os.urandom(32)

users = {"userNow": "userNowPass"}

@app.route("/login", methods = ["GET", "POST"])
def login():
    #person is currently logged in
    if(session.has.key("username")):
        return render_template("home.html")

    #if the participant has just logged in
    userNow = request.form["username"]
    userNowPass = request.form["password"]
    #if the account and such match
    if(userNow in users.keys()) && (users[userNow] == userNowPass):
        session["username"] = userNow
        return render_template("home.html")
    #if password is incorrect
    elif(userNow in users.keys()):
        flash("Wrong password")
        return render_template("login.html")
    #if account does not exist
    else:
        flash("Press Register to create a new account, boy")
        return render_template("login.html")
    
