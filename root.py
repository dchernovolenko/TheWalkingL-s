#importing all of the necessary equipment
from flask import Flask, render_template, request, session, redirect, url_for, flash
#to run urandom
import os
import sqlite3
from utils import sqlite3lib


app = Flask(__name__)
#hashes the key into a random sequence
app.secret_key = os.urandom(32)

# database connection
db_name = "data/thewalkingls.db"
db = sqlite3.connect(db_name, check_same_thread=False)

#users: the library containing all of the users
#userNow: essentially the "dummy user," with userNowPass as password
users = {"userNow": "userNowPass"}

#the root route
#no specific html file; defaults to either home or login.html
@app.route("/", methods = ["GET", "POST"])
def root():
    #if you are logged in
    if(session.has_key("username")):
        return redirect(url_for("home"))
    #login page
    else:
        return render_template("login.html")

#the login route
#if user is logged in, it defaults to home.html
@app.route("/login", methods = ["GET", "POST"])
def login():
    #if the participant has just logged in
    userNow = request.form["username"]
    userNowPass = request.form["password"]
    #if the account and such match
    if(userNow in users.keys()) and (users[userNow] == userNowPass):
        session["username"] = userNow
        return redirect(url_for("home"))
    #if password is incorrect
    elif(userNow in users.keys()):
        flash("Wrong password")
        return redirect(url_for("root"))
    elif(request.form["registerButton"] == "Register"):
        return render_template("signup.html")
    #if account does not exist
    else:
        flash("Press Register to create a new account, boy")
        return render_template("login.html")

#used to register a new account within the session
@app.route("/signup", methods = ["GET", "POST"])
def signup():
    #user information for the new account
    newUser = request.form["newUser"]
    newPass = request.form["newPass"]
    if(newUser in users.keys()):
        #handles th case of the account already existing
        flash("Bad, this account exist")
        return render_template("signup.html")
    elif (newUser == ""):
        return render_template("signup.html")
    else:
        #also automatically logs the user in
        session["username"] = newUser
        users[newUser] = newPass
        return redirect(url_for("home"))

@app.route("/home", methods = ["GET", "POST"])
def home():
    if("username" in session.keys()):
        return render_template("home.html", user = session["username"])
    else:
        return redirect(url_for("root"))

#the edit route
@app.route("/edit", methods = ["GET", "POST"])
def edit():
    '''
    test
    '''
    story_id = request.args["story_id"]
    story_info = sqlite3lib.get_story_info(db, story_id)
    s_title = story_info["title"]
    s_creator = sqlite3lib.get_user_info(db, story_info["owner"])["username"]
    s_story = story_info["story"]
    # to edit run add_to_story(dbh, story), call it in read_story() and use request.args()
    return render_template("story.html", title=s_title, creator=s_creator, story=s_story, time="sometime", reading = FALSE)

@app.route("/create", methods = ["GET", "POST"])
def create():
    user_id = request.args["user_id"]
    catList = sqlite3lib.get_categories(db)
    # to run create_new_story(dbh, args), call it in read_story() and use request.args()
    return render_template("newstory.html", categories = catList)


@app.route("/read", methods = ["GET", "POST"])
def read():
    # run create_story(dbh, args) if you have come from newstory.html, run add_to_story if otherwise
    if request.args["submission"] == "new_story":
        s_creator = session["username"]
        s_title = request.args["title"]
        s_category = request.args["category"]
        s_story = request.args["story"]
        sqlite3lib.create_story(db, s_creator, s_title, s_category)
    else:
        story_id = request.args["story_id"]
        story_info = sqlite3lib.get_story_info(db, story_id)
        s_title = story_info["title"]
        s_creator = get_user_info(db, story_info["owner"])["username"]
        sqlite3lib.add_to_story(db, s_creator, story_id, request.args["story"])
        s_story = sqlite3lib.get_story(db, story_id)
    return render_template("story.html", title=s_title, creator=s_creator, story=s_story, time="sometime", reading = TRUE)

@app.route("/categories", methods = ["GET", "POST"])
def categories():
    # make a list of all the categories
    catList = sqlite3lib.get_categories(db)
    return render_template("categories.html", categories = catList)

@app.route("/category", methods = ["GET", "POST"])
def category():
    storyList = []
    for i in range(0, 16):
        storyList.append(get_story_info(db, i))
    return render_template("category.html", stories = storyList)

@app.route("/logout", methods = ["GET", "POST"])
def logout():
    session.pop("username")
    users = {"userNow": "userNowPass"}
    return redirect(url_for("root"))

if __name__ == "__main__":
    app.debug = True
    app.run()

    # close database connection
    db.close()
