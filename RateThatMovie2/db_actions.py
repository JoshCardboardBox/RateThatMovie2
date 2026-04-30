#imports
from tlbx_imports import *





def get_movies():
    cur.execute("SELECT * FROM movies;")
    movs = cur.fetchall()
    return movs

def get_genres():
    cur.execute("SELECT * FROM genres;")
    genres = cur.fetchall()
    return genres



# Accounts / Users
def check_user_exists(user_id):
    cur.execute("SELECT * FROM users WHERE user_id=%s", [user_id])
    if cur.rowcount != 0:
        return True
    else:
        return False


#USER DATABASE ACTIONS (get x)
def get_user_id(email, password):
    cur.execute("SELECT user_id FROM users WHERE email=%s AND password=%s", [email, password])

    #return id if you found it
    if cur.rowcount != 0:
        return int(cur.fetchone()['user_id'])
    else:
        return None

def get_user_username(user_id):
    cur.execute("SELECT username FROM users WHERE user_id=%s", [user_id])
    username = cur.fetchone()['username']
    return username

def get_user_password(user_id):
    cur.execute("SELECT password FROM users WHERE user_id=%s", [user_id])
    password = cur.fetchone()['password']
    return password

def get_user_email(user_id):
    cur.execute("SELECT email FROM users WHERE user_id=%s", [user_id])
    email = cur.fetchone()['email']
    return email

#CREATING USER
def create_user(username, email, password):
    #do-while loop to generate user_id, keep doing until unique one found...
    unique_id_found = False
    user_id = 0
    while(not unique_id_found):
        user_id = random.randint(1, 1000000)
        cur.execute("SELECT count(*) FROM users WHERE user_id=%s", [user_id])
        matches = cur.fetchone()['count'] #get dictionary, then take int out of dictionary type
        #if you've found a user_id number that no account uses, then continue on...
        if matches == 0:
            unique_id_found = True


    #CREATE THE ACCOUNT
    cur.execute("INSERT INTO users (user_id, username, email, password) VALUES (%s, %s, %s, %s);", [user_id, username, email, password])
    conn.commit()

#Checks if the entered username or email already matches that of another user
# True if match found
def check_username_email_matches(username, email):
    cur.execute("SELECT count(*) FROM users WHERE username=%s", [username])
    matches = cur.fetchone()['count']
    if matches != 0:
        return True

    cur.execute("SELECT count(*) FROM users WHERE email=%s", [email])
    matches = cur.fetchone()['count']
    if matches != 0:
        return True

    return False


#Input Validation
# ensured to prevent illogical SQL statements from being run
def security_input(input):
    #remove all semicolons (;)
    if ";" in input:
        input = input.replace(";", "")
    return input



#Database reviews add and get them

#stores which user reviewed what movie
def add_review(user_id, movie_id, rating, review_text):
    cur.execute(
        """ INSERT INTO reviews (user_id, movie_id, rating, review_text) VALUES (%s, %s, %s, %s)"""
        , [user_id, movie_id, rating, review_text] )
    conn.commit()


#gets the reviews from database
#joins users and the movie table so the username and titles show instead of ids
def get_all_reviews():
    cur.execute(
        """ SELECT
            users.username, movies.title, reviews.rating, reviews.review_text, reviews.created_at
        FROM reviews JOIN users ON  reviews.user_id =  users.user_id JOIN movies ON reviews.movie_id = movies.movie_id
        ORDER BY  reviews.created_at DESC""" )
    return cur.fetchall()


#dropdown table
#displays movies in alphabetical order
def get_movie_options():
    cur.execute("SELECT movie_id, title FROM movies ORDER BY title")
    return cur.fetchall()