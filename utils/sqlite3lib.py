import sqlite3

def db_exec(dbh, sql_funct):
    '''
    Prereq:
    dbh is the database connection
    sql_funt is an sql command or one of the table functions below

    Funct:
    Executes and commits command to database
    '''
    c = dbh.cursor()
    command = sql_funct
    c.execute(command)
    print command
    dbh.commit()

def db_exec_fetch(dbh, sql_funct):
    '''
    Funct:
    Executes and commits command to database.
    Returns list of querey elements.
    '''
    c = dbh.cursor()
    command = sql_funct
    ex = c.execute(command)
    print command
    return ex.fetchall()

def get_users(dbh):
    '''
    Funct:
    Returns dictionary of usernames: password
    '''
    command = "SELECT username, hash_pass FROM user_pass;"
    c = dbh.cursor()
    x = c.execute(command)
    users = {}
    for line in x:
        users[line[0]] = line[1]
    return users

def get_user_info(dbh, user_id):
    user_info_fetch = db_exec_fetch(dbh, select_user_info(user_id))[0]
    user_info = {'user_id': user_info_fetch[0],
                 'username': user_info_fetch[1],
                 'hash_pass': user_info_fetch[2]}
    print user_info
    
def get_user_story_ids(dbh, user_id):
    '''
    returns list of story_ids of user's stories
    '''
    story_ids= []
    user_story_fetch = db_exec_fetch(dbh, "SELECT story_id FROM user_stories WHERE user_id = %i" % (user_id))
    print user_story_fetch
    for i in user_story_fetch:
        story_ids.append(i[0])
    return story_ids

def get_story(dbh, story_id):
    story_fetch = db_exec_fetch(dbh, select_story(story_id))
    return story_fetch[0][0]

def get_story_info(dbh, story_id):
    '''
    returns dictionary of story_info
    '''
    story_info_fetch = db_exec_fetch(dbh, "SELECT * FROM stories WHERE story_id = %i" % (story_id))[0]
    story_info = {'story_id': story_info_fetch[0],
                  'title': story_info_fetch[1],
                  'category': story_info_fetch[2],
                  'story': story_info_fetch[3]
                  }
    return story_info
    
def create_story(dbh, user_id, title, category):
    '''
    Prereq:
    Uses aft_insert trigger in db_init.py

    Funct:
    Creates new story
    '''
    db_exec(dbh, insert_new_story(title,category))
    db_exec(dbh, set_user_story_userid(user_id))
    
def write_story(dbh, story_id, text):
    '''
    Prereq:
    Story exists

    Funct:
    Sets text of story based on story_id
    '''
    old_story = db_exec_fetch(dbh, select_story(story_id))
    new_story = ""
    if old_story[0][0] == None:
        new_story = text
    else:
        new_story = old_story[0][0] + " " + text
    db_exec(dbh, update_story(story_id, new_story))

def add_to_story(dbh, user_id, story_id, text):
    '''
    Prereq:
    Story exists

    Funct:
    Adds to story
    Creates new row in user_stories with user_id, story_id, and ownership=2
    '''
    db_exec(dbh, insert_new_user_story(user_id, story_id, 2))
    write_story(dbh, story_id, text)

    
# --------------------------- BASIC SQL FUNCTIONS ------------------------------
# user_pass table functions
def insert_new_user(user, hash_pass):
    '''
    Prereq:
    User does nnot exist in database.
    Password is already hashed.
    '''
    return "INSERT INTO user_pass VALUES (null,'%s','%s');" % (user, hash_pass)
 
def update_user_pass(user_id, hash_pass):
    '''
    Prereq:
    User exists.
    '''
    return "UPDATE user_pass SET hash_pass = '%s' WHERE user_id = %i;" % (hash_pass, user_id)

def select_user_info(user_id):
    return "SELECT * FROM user_pass WHERE user_id = %i" % (user_id)

# user_stories table functions
def insert_new_user_story(user_id, story_id, owner):
    return "INSERT INTO user_stories VALUES (%i,%i,%i);" % (user_id, story_id, owner)

def set_user_story_userid(user_id):
    return "UPDATE user_stories SET user_id = %i" % (user_id)

def set_user_story_ownership(user_id, ownership):
    return "UPDATE user_stories SET ownership = %i WHERE user_id = %i" % (ownership, user_id)

def select_ownership(user_id, story_id):
    return "SELECT ownership FROM user_stories WHERE user_id = %i AND story_id = %i;" % (user_id, story_id)

def select_user_story(user_id, story_id):
    '''
    TEST
    '''
    return "SELECT story FROM stories WHERE user_stories.story_id = %i AND user_stories.user_id = %i;" % (story_id, user_id)

# stories table functions
def insert_new_story(title, category):
    return "INSERT INTO stories VALUES (null, '%s', '%s', null);" % (title, category)

def update_story(story_id, text):
    return "UPDATE stories SET story = '%s' WHERE story_id = %i;" % (text, story_id)

def select_story(story_id):
    return "SELECT story FROM stories WHERE story_id = %i" % (story_id)

def update_title(story_id, new_title):
    return "UPDATE stories SET title = '%s' WHERE story_id = %i" % (new_title, story_id)

def update_category(story_id, new_category):
    return "UPDATE stories SET category = '%s' WHERE story_id = %i" % (new_category, story_id)


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
    story = db_exec_fetch(db, get_story(1))
    print story
    db_exec(db, write_story(1, 'hi there'))
    '''

    #py funct
    '''
    create_story(db, 1, "J", "Fiction")
    write_story(db, 1, "They walked") 
    add_to_story(db, 2, 1, " The castle on the hill.")
    print get_story_info(db, 1);
    print get_user_story_ids(db, 1)
    print get_story(db, 1)
    print get_user_info(db, 1)
    '''

    
    db.close()
