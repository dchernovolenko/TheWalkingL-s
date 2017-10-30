from flask import Flask, render_template, request, session, redirect, url_for
import os
from utils import sqlite3lib
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(32)

# database connection
db_name = "data/thewalkingls.db"
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
    s_creator = get_user_info(db, story_info["owner"])["username"]
    s_story = story_info["story"]
    # to edit run add_to_story(dbh, story), call it in read_story() and use request.args()
    return render_template("story.html", title=s_title, creator=s_creator, story=s_story, time="sometime", reading = FALSE)

@app.route("/create", methods = ["GET", "POST"])
def create():
    user_id = request.args["user_id"]
    catList = get_categories(db)
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
        create_story(db, s_creator, s_title, s_category)
    else:
        story_id = request.args["story_id"]
        story_info = get_story_info(db, story_id)
        s_title = story_info["title"]
        s_creator = get_user_info(db, story_info["owner"])["username"]
        add_to_story(db, s_creator, story_id, request.args["story"])
        s_story = get_story(db, story_id)
    return render_template("story.html", title=s_title, creator=s_creator, story=s_story, time="sometime", reading = TRUE)

@app.route("/categories", methods = ["GET", "POST"])
def categories():
    # make a list of all the categories
    catList = get_categories(db)
    return render_template("categories.html", categories = catList)

@app.route("/category", methods = ["GET", "POST"])
def category():
    storyList = []
    for i in range(0, 16):
        storyList.append(get_story_info(db, i))
    return render_template("category.html", stories = storyList)

if __name__ == "__main__":
    app.debug = True
    app.run()

    # close database connection
    db.close()
