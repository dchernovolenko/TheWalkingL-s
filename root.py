#importing all of the necessary equipment
from flask import Flask, render_template, request, session, redirect, url_for, flash
import hashlib
#to run urandom
import os
import sqlite3
from utils import sqlite3lib

app = Flask(__name__)
#hashes the key into a random sequence
app.secret_key = os.urandom(32)
def hasher(password):
	hashed = hashlib.md5(password.encode())
	print hashed.hexdigest()
	return hashed.hexdigest()
	
# database connection
db_name = "data/thewalkingls.db"
db = sqlite3.connect(db_name, check_same_thread=False)

#users: the library containing all of the users
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
    users = sqlite3lib.get_users(db)
    #if the participant has just logged in
    userNow = request.form["username"]
    userNowPass = hasher(request.form["password"])
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
    users = sqlite3lib.get_users(db)
    #user information for the new account
    newUser = request.form["newUser"]
    newPass = hasher(request.form["newPass"])
    if(newUser in users.keys()):
        #handles th case of the account already existing
        flash("Bad, this account exist")
        return render_template("login.html")
    else:
        #also automatically logs the user in
        sqlite3lib.add_user(db, newUser, newPass)
    return redirect("/")

@app.route("/home", methods = ["GET", "POST"])
def home():
    ids = sqlite3lib.get_ids(db)
    idofuser = ids[session["username"]]
    storyids = sqlite3lib.get_user_story_ids(db, idofuser)
    stors = {}
    for x in storyids:
        d = sqlite3lib.get_story_info(db,x)
        stors[d["title"]] = x
    return render_template("home.html",stories = stors, user = session["username"])


#the edit route
@app.route("/edit", methods = ["GET", "POST"])
def edit():
    story_id = request.args["story_id"]
    story_id = int(story_id)
    story_info = sqlite3lib.get_story_info(db, story_id)
    s_title = story_info["title"]
    s_last = story_info["lastsub"]
    print s_last
    s_creatorhelp = story_info["owner"]
    s_creatorhelp2 = sqlite3lib.get_user_info(db, s_creatorhelp)
    s_creator = s_creatorhelp2["username"]
    #sqlite3lib.add_to_story(db, s_creator, story_id, request.args["story"])
    s_story = sqlite3lib.get_story(db, story_id)
    # to edit run add_to_story(dbh, story), call it in read_story() and use request.args()
    return render_template("story.html", title=s_title, creator=s_creator, storylast= s_last, time="sometime", reading = "false", s_id = story_id)

@app.route("/edithelp", methods = ["GET", "POST"])
def edithelp():
    story_id = int(request.args["story_id"])
    ids = sqlite3lib.get_ids(db)
    idofuser = ids[session["username"]]
    story_info = sqlite3lib.get_story_info(db, story_id)
    s_title = story_info["title"]
    s_creatorhelp = story_info["owner"]
    s_creatorhelp2 = sqlite3lib.get_user_info(db, s_creatorhelp)
    s_creator = s_creatorhelp2["username"]
    sqlite3lib.add_to_story(db, idofuser , story_id, request.args["story"])
    s_story = sqlite3lib.get_story(db, story_id)
    return redirect(url_for("home"))

@app.route("/create", methods = ["GET", "POST"])
def create():
    catList = sqlite3lib.get_categories(db)
    # to run create_new_story(dbh, args), call it in read_story() and use request.args()
    return render_template("newstory.html", categories = catList)

@app.route("/read", methods = ["GET", "POST"])
def read():
    # run create_story(dbh, args) if you have come from newstory.html, run add_to_story if otherwise
    try:
        if request.args["submission"] == "new_story":
            ids = sqlite3lib.get_ids(db)
            idofuser = ids[session["username"]]
            print "test"
            print session["username"]
            s_creator = idofuser
            print s_creator
            s_title = request.args["title"]
            print s_title
            s_category = request.args["category"]
            print s_category
            s_story = request.args["story"]
            print s_story
            sqlite3lib.create_story(db, s_creator, s_title, s_category, s_story)
            print "test6"
    except:
            s = request.args["story_id"]
            story_id = int(s)
            story_info = sqlite3lib.get_story_info(db, story_id)
            s_title = story_info["title"]
            s_creatorhelp = story_info["owner"]
            s_creatorhelp2 = sqlite3lib.get_user_info(db, s_creatorhelp)
            s_creator = s_creatorhelp2["username"]
            #sqlite3lib.add_to_story(db, s_creator, story_id, request.args["story"])
            s_story = sqlite3lib.get_story(db, story_id)

    return render_template("story.html", title=s_title, creator=session["username"], story=s_story, reading = "true")

@app.route("/category", methods = ["GET", "POST"])
def category():
    storyList = []
    for i in range(0, 5):
        try:
            storyList.append(sqlite3lib.get_story_info(db, i))
        except:
            pass
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
