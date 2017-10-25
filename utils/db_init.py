import sqlite3
import csv

try:
    execfile("../data/db_builder.py")
except:
    pass

# create tables
# table1 - usernames and passwords
def create_user_pass_table():
    c.execute("CREATE TABLE user_pass (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, hash_pass TEXT);")
    print "CREATED USER_PASS TABLE"

# table2 - users and stories
def create_user_stories_table():
    c.execute("CREATE TABLE user_stories (user_id INTEGER KEY, story_id INTEGER KEY, ownership INTEGER);")
    print "CREATED USER_STORIES TABLE"

# table3 - stories
def create_stories_table():
    c.execute("CREATE TABLE stories (story_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, category TEXT, story TEXT);")
    print "CREATED STORIES TABLE"

if __name__ == "__main__":
    db_name = "../data/thewalkingls.db"
    db = sqlite3.connect(db_name)
    c = db.cursor()
    
    create_user_pass_table()
    create_user_stories_table()
    create_stories_table()
    
    db.commit()
    db.close()
