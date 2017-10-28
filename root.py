from flask import Flask, render_template, request, session, redirect, url_for
import os
from utils import sqlite3lib

app = Flask(__name__)
app.secret_key = os.urandom(32)

# database connection
db_name = "../data/thewalkingls.db"
db = sqlite3.connect(db_name)

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

@app.route("/edit", methods = ["GET", "POST"])
def edit():
    '''
    test
    '''
    story_id = request.args["story_id"]
    story_info = get_story_info(db, story_id)
    s_title = story_info["title"]
    s_creator = story_info["owner"]
    s_story = story_info["story"]
    # to edit run add_to_story(dbh, story), call it in read_story() and use request.args()
    return render_template("story.html", title=s_title, creator=s_creator, story=s_story, time="sometime") 

@app.route("/create", methods = ["GET", "POST"])
def create():
    user_id = request.args["user_id"]
    # to run create_new_story(dbh, args), call it in read_story() and use request.args()
    return render_template("newstory.html", user_id)

if __name__ == "__main__":
    app.debug = True
    app.run()
    
    # close database connection
    db.close()
    
