import sqlite3

def db_exec(dbh, sql_funct):
    '''
    Prereq:
    dbh is the database connection
    sql_funt is an sql command or one of the functions below

    Funct:
    Executes anc commits command to database
    '''
    c = dbh.cursor()
    command = sql_funct
    c.execute(command)
    print command
    dbh.commit()
    
# user_pass table functions
def insert_new_user(user, hash_pass):
    '''
    Prereq:
    User does nnot exist in database.
    Password is already hashed.

    Funct:
    Adds new row of user and hashed password.
    '''
    return "INSERT INTO user_pass VALUES (null,'%s','%s');" % (user, hash_pass)
 
def update_user_pass(user, hash_pass):
    '''
    Prereq:
    User exists.

    Funt:
    Updates userpassword
    '''
    return "UPDATE user_pass SET hash_pass = '%s' WHERE [username = '%s'];" % (hash_pass, user)


if __name__ == "__main__":
    db_name = "../data/thewalkingls.db"
    db = sqlite3.connect(db_name)

    db_exec(db, insert_new_user("L", "hi"));
    
    #c = db.cursor()
    #insert_new_user("J", "Pass")
    #db.commit()
    
    db.close()
