from tlbx_imports import *
import psycopg2
import psycopg2.extras

# ---------------------------------------------------------
# KEEP YOUR EXISTING conn AND cur ABOVE THIS LINE
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


# Convenience wrappers
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
# FULL CREW (crew table)
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