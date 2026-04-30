#imports
from tlbx_imports import *
import psycopg2
import psycopg2.extras

# ---------------------------------------------------------
# KEEP YOUR EXISTING CONNECTION ABOVE THIS LINE
# ---------------------------------------------------------


# ---------------------------------------------------------
# MOVIE DETAILS
# ---------------------------------------------------------
def get_movie_details(movie_id):
    try:
        cur.execute("""
            SELECT movie_id, title, release_date, runtime, budget, revenue,
                   status, adult, original_language, genres
            FROM movies
            WHERE movie_id = %s;
        """, [movie_id])
        return cur.fetchone()
    except Exception as e:
        print("GET MOVIE DETAILS ERROR:", e)
        return None


# ---------------------------------------------------------
# SEARCH MOVIES
# ---------------------------------------------------------
def search_movies(query):
    try:
        pattern = f"%{query}%"
        cur.execute("""
            SELECT movie_id, title, release_date
            FROM movies
            WHERE LOWER(title) LIKE LOWER(%s)
            ORDER BY release_date DESC
            LIMIT 50;
        """, [pattern])
        return cur.fetchall()
    except Exception as e:
        print("SEARCH MOVIES ERROR:", e)
        return []


# ---------------------------------------------------------
# SEARCH ACTORS
# ---------------------------------------------------------
def search_actors(query):
    try:
        pattern = f"%{query}%"
        cur.execute("""
            SELECT DISTINCT p.person_id, p.name
            FROM persons p
            JOIN actors a ON a.person_id = p.person_id
            WHERE LOWER(p.name) LIKE LOWER(%s)
            ORDER BY p.name
            LIMIT 50;
        """, [pattern])
        return cur.fetchall()
    except Exception as e:
        print("SEARCH ACTORS ERROR:", e)
        return []


# ---------------------------------------------------------
# SEARCH DIRECTORS (crew-based)
# ---------------------------------------------------------
def search_directors(query):
    try:
        pattern = f"%{query}%"
        cur.execute("""
            SELECT DISTINCT p.person_id AS director_id, p.name
            FROM crew c
            JOIN persons p ON p.person_id = c.person_id
            WHERE LOWER(c.job) = 'director'
              AND LOWER(p.name) LIKE LOWER(%s)
            ORDER BY p.name
            LIMIT 50;
        """, [pattern])
        return cur.fetchall()
    except Exception as e:
        print("SEARCH DIRECTORS ERROR:", e)
        return []


# ---------------------------------------------------------
# ACTOR DETAILS
# ---------------------------------------------------------
def get_actor_details(person_id):
    try:
        cur.execute("""
            SELECT person_id, name
            FROM persons
            WHERE person_id = %s;
        """, [person_id])
        return cur.fetchone()
    except Exception as e:
        print("GET ACTOR DETAILS ERROR:", e)
        return None


# ---------------------------------------------------------
# DIRECTOR DETAILS (crew-based)
# ---------------------------------------------------------
def get_director_details(person_id):
    try:
        cur.execute("""
            SELECT person_id AS director_id, name
            FROM persons
            WHERE person_id = %s;
        """, [person_id])
        return cur.fetchone()
    except Exception as e:
        print("GET DIRECTOR DETAILS ERROR:", e)
        return None


# ---------------------------------------------------------
# MOVIES BY ACTOR
# ---------------------------------------------------------
def get_movies_by_actor(person_id):
    try:
        cur.execute("""
            SELECT m.movie_id, m.title, m.release_date, a.character
            FROM actors a
            JOIN movies m ON m.movie_id = a.movie_id
            WHERE a.person_id = %s
            ORDER BY m.release_date DESC;
        """, [person_id])
        return cur.fetchall()
    except Exception as e:
        print("GET MOVIES BY ACTOR ERROR:", e)
        return []


# ---------------------------------------------------------
# MOVIES BY DIRECTOR (crew-based)
# ---------------------------------------------------------
def get_movies_by_director(person_id):
    try:
        cur.execute("""
            SELECT m.movie_id, m.title, m.release_date
            FROM crew c
            JOIN movies m ON m.movie_id = c.movie_id
            WHERE c.person_id = %s
              AND LOWER(c.job) = 'director'
            ORDER BY m.release_date DESC;
        """, [person_id])
        return cur.fetchall()
    except Exception as e:
        print("GET MOVIES BY DIRECTOR ERROR:", e)
        return []


# ---------------------------------------------------------
# FULL CAST
# ---------------------------------------------------------
def get_full_cast(movie_id):
    try:
        cur.execute("""
            SELECT p.person_id, p.name, a.character, a.cast_order
            FROM actors a
            JOIN persons p ON p.person_id = a.person_id
            WHERE a.movie_id = %s
            ORDER BY a.cast_order ASC;
        """, [movie_id])
        return cur.fetchall()
    except Exception as e:
        print("GET FULL CAST ERROR:", e)
        return []


# ---------------------------------------------------------
# FULL CREW
# ---------------------------------------------------------
def get_full_crew(movie_id):
    try:
        cur.execute("""
            SELECT p.person_id, p.name, c.job, c.department
            FROM crew c
            JOIN persons p ON p.person_id = c.person_id
            WHERE c.movie_id = %s
            ORDER BY c.department, c.job, p.name;
        """, [movie_id])
        return cur.fetchall()
    except Exception as e:
        print("GET FULL CREW ERROR:", e)
        return []


# ---------------------------------------------------------
# FAVORITES (UNIFIED)
# ---------------------------------------------------------
def add_favorite_item(user_id, item_type, item_id):
    try:
        cur.execute("""
            INSERT INTO favorites (user_id, item_type, item_id)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, item_type, item_id) DO NOTHING;
        """, [user_id, item_type, item_id])
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print("ADD FAVORITE ITEM ERROR:", e)
        return False


def remove_favorite_item(user_id, item_type, item_id):
    try:
        cur.execute("""
            DELETE FROM favorites
            WHERE user_id=%s AND item_type=%s AND item_id=%s;
        """, [user_id, item_type, item_id])
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print("REMOVE FAVORITE ITEM ERROR:", e)
        return False


def is_favorited_item(user_id, item_type, item_id):
    try:
        cur.execute("""
            SELECT 1
            FROM favorites
            WHERE user_id=%s AND item_type=%s AND item_id=%s;
        """, [user_id, item_type, item_id])
        return cur.fetchone() is not None
    except Exception as e:
        print("IS FAVORITED ITEM ERROR:", e)
        return False


def get_favorite_movies(user_id):
    try:
        cur.execute("""
            SELECT f.item_id AS movie_id, m.title, m.release_date
            FROM favorites f
            JOIN movies m ON m.movie_id = f.item_id
            WHERE f.user_id=%s AND f.item_type='movie';
        """, [user_id])
        return cur.fetchall()
    except Exception as e:
        print("GET FAVORITE MOVIES ERROR:", e)
        return []


def get_favorite_actors(user_id):
    try:
        cur.execute("""
            SELECT f.item_id AS person_id, p.name
            FROM favorites f
            JOIN persons p ON p.person_id = f.item_id
            WHERE f.user_id=%s AND f.item_type='actor';
        """, [user_id])
        return cur.fetchall()
    except Exception as e:
        print("GET FAVORITE ACTORS ERROR:", e)
        return []


def get_favorite_directors(user_id):
    try:
        cur.execute("""
            SELECT f.item_id AS director_id, p.name
            FROM favorites f
            JOIN persons p ON p.person_id = f.item_id
            WHERE f.user_id=%s AND f.item_type='director';
        """, [user_id])
        return cur.fetchall()
    except Exception as e:
        print("GET FAVORITE DIRECTORS ERROR:", e)
        return []


# ---------------------------------------------------------
# RATINGS
# ---------------------------------------------------------
def set_rating_item(user_id, item_type, item_id, rating):
    try:
        cur.execute("""
            INSERT INTO ratings (user_id, item_type, item_id, rating)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (user_id, item_type, item_id)
            DO UPDATE SET rating = EXCLUDED.rating;
        """, [user_id, item_type, item_id, rating])
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print("SET RATING ERROR:", e)
        return False


def get_rating_item(user_id, item_type, item_id):
    try:
        cur.execute("""
            SELECT rating
            FROM ratings
            WHERE user_id=%s AND item_type=%s AND item_id=%s;
        """, [user_id, item_type, item_id])
        row = cur.fetchone()
        return row['rating'] if row else None
    except Exception as e:
        print("GET RATING ERROR:", e)
        return None


def get_average_rating(item_type, item_id):
    try:
        cur.execute("""
            SELECT AVG(rating)::numeric(10,2) AS avg_rating
            FROM ratings
            WHERE item_type=%s AND item_id=%s;
        """, [item_type, item_id])
        row = cur.fetchone()
        return float(row['avg_rating']) if row and row['avg_rating'] else None
    except Exception as e:
        print("GET AVG RATING ERROR:", e)
        return None

#OTHER CODE

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