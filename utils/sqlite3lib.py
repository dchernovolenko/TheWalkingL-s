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
    return "UPDATE user_pass SET hash_pass = '%s' WHERE username = '%s';" % (hash_pass, user)

# stories table functions
def create_story(title, category):
    '''
    Funct:
    Create new row in stories table
    '''
    return "INSERT INTO stories VALUES (null, '%s', '%s', '');" % (title, category)

def write_story(story_id, text):
    '''
    Funct:
    Adds more story to an existing story
    '''
    return "UPDATE stories SET story = story+'%s' WHERE story_id = %i;" % (text, story_id)

def ret_story(story_id):
    '''
    Funct:
    db cursor selects story based on story id
    '''
    return "SELECT story from stories WHERE story_id = %i;" % (story_id)
    
if __name__ == "__main__":
    db_name = "../data/thewalkingls.db"
    db = sqlite3.connect(db_name)

    # user_pass testing
    '''
    db_exec(db, insert_new_user("L", "hi"))
    db_exec(db, update_user_pass("L", "hi"))
    '''

    # stories testing
    '''
    db_exec(db, create_story("The walking", "Fiction"))
    '''
    db_exec(db, write_story(1, "They walked."))
    
    db.close()
