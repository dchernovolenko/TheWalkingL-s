import sqlite3

db_name = "thewalkingls.db"
db = sqlite3.connect(db_name)
c = db.cursor()

# user_pass table functions
def insert_new_user(user, hash_pass):
    c.execute("INSERT INTO user_pass VALUES (%s,%s)" % (user, hash_pass))
    
