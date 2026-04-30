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
# UNIVERSAL DIRECTOR SEARCH
# ---------------------------------------------------------
def search_directors(query):
    try:
        pattern = f"%{query}%"

        # 1️⃣ Search directors table
        cur.execute("""
            SELECT director_id, name
            FROM directors
            WHERE LOWER(name) LIKE LOWER(%s)
        """, [pattern])
        directors_table = cur.fetchall()

        # 2️⃣ Search crew table for job='Director'
        cur.execute("""
            SELECT DISTINCT p.person_id AS director_id, p.name
            FROM crew c
            JOIN persons p ON p.person_id = c.person_id
            WHERE LOWER(c.job) = 'director'
              AND LOWER(p.name) LIKE LOWER(%s)
        """, [pattern])
        crew_directors = cur.fetchall()

        # 3️⃣ Merge results (avoid duplicates)
        seen = set()
        results = []

        for d in directors_table + crew_directors:
            if d['director_id'] not in seen:
                seen.add(d['director_id'])
                results.append(d)

        return results[:50]

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
# DIRECTOR DETAILS (works for both tables)
# ---------------------------------------------------------
def get_director_details(director_id):
    try:
        # Try directors table first
        cur.execute("""
            SELECT director_id, name
            FROM directors
            WHERE director_id = %s;
        """, [director_id])
        d = cur.fetchone()
        if d:
            return d

        # Try persons table (crew-based directors)
        cur.execute("""
            SELECT person_id AS director_id, name
            FROM persons
            WHERE person_id = %s;
        """, [director_id])
        return cur.fetchone()

    except Exception as e:
        print("GET DIRECTOR DETAILS ERROR:", e)
        return None


# ---------------------------------------------------------
# MOVIES BY DIRECTOR (works for both tables)
# ---------------------------------------------------------
def get_movies_by_director(director_id):
    try:
        # 1️⃣ directors table
        cur.execute("""
            SELECT m.movie_id, m.title, m.release_date
            FROM movie_directors md
            JOIN movies m ON m.movie_id = md.movie_id
            WHERE md.director_id = %s
            ORDER BY m.release_date DESC;
        """, [director_id])
        movies = cur.fetchall()

        # 2️⃣ crew table fallback
        cur.execute("""
            SELECT m.movie_id, m.title, m.release_date
            FROM crew c
            JOIN movies m ON m.movie_id = c.movie_id
            WHERE c.person_id = %s
              AND LOWER(c.job) = 'director'
            ORDER BY m.release_date DESC;
        """, [director_id])
        movies += cur.fetchall()

        # Remove duplicates
        seen = set()
        final = []
        for m in movies:
            if m['movie_id'] not in seen:
                seen.add(m['movie_id'])
                final.append(m)

        return final

    except Exception as e:
        print("GET MOVIES BY DIRECTOR ERROR:", e)
        return []


# ---------------------------------------------------------
# FAVORITES
# ---------------------------------------------------------
def add_favorite(user_id, movie_id):
    try:
        cur.execute("""
            INSERT INTO favorites (user_id, movie_id)
            VALUES (%s, %s)
            ON CONFLICT (user_id, movie_id) DO NOTHING;
        """, [user_id, movie_id])
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print("ADD FAVORITE ERROR:", e)
        return False


def remove_favorite(user_id, movie_id):
    try:
        cur.execute("""
            DELETE FROM favorites
            WHERE user_id=%s AND movie_id=%s;
        """, [user_id, movie_id])
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print("REMOVE FAVORITE ERROR:", e)
        return False


def is_favorited(user_id, movie_id):
    try:
        cur.execute("""
            SELECT 1 FROM favorites
            WHERE user_id=%s AND movie_id=%s;
        """, [user_id, movie_id])
        return cur.fetchone() is not None
    except Exception as e:
        print("IS FAVORITED ERROR:", e)
        return False


def get_favorite_movies(user_id):
    try:
        cur.execute("""
            SELECT movie_id
            FROM favorites
            WHERE user_id=%s;
        """, [user_id])
        return cur.fetchall()
    except Exception as e:
        print("GET FAVORITES ERROR:", e)
        return []