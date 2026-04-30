# favoriting.py

from tlbx_imports import *
from db_actions import cur, conn


# ---------------------------------------------------------
# ADD FAVORITE (MOVIES ONLY)
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


# ---------------------------------------------------------
# REMOVE FAVORITE
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# CHECK IF FAVORITED
# ---------------------------------------------------------
def is_favorited(user_id, movie_id):
    try:
        cur.execute("""
            SELECT 1 FROM favorites
            WHERE user_id=%s AND movie_id=%s;
        """, [user_id, movie_id])
        return cur.fetchone() is not None
    except Exception as e:
        conn.rollback()
        print("IS FAVORITED ERROR:", e)
        return False


# ---------------------------------------------------------
# GET ALL FAVORITE MOVIES FOR A USER
# ---------------------------------------------------------
def get_favorite_movies(user_id):
    try:
        cur.execute("""
            SELECT movie_id
            FROM favorites
            WHERE user_id=%s;
        """, [user_id])
        return cur.fetchall()
    except Exception as e:
        conn.rollback()
        print("GET FAVORITES ERROR:", e)
        return []
'''
def add_favorite(user_id, item_type, item_id):
    try:
        cur.execute("""
            INSERT INTO favorites (user_id, item_type, item_id)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, item_type, item_id) DO NOTHING;
        """, [user_id, item_type, item_id])
        conn.commit()
        return {"message": "Added to favorites"}
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}


def remove_favorite(user_id, item_type, item_id):
    try:
        cur.execute("""
            DELETE FROM favorites
            WHERE user_id=%s AND item_type=%s AND item_id=%s;
        """, [user_id, item_type, item_id])
        conn.commit()
        return {"message": "Removed from favorites"}
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}


def is_favorited(user_id, item_type, item_id):
    try:
        cur.execute("""
            SELECT 1 FROM favorites
            WHERE user_id=%s AND item_type=%s AND item_id=%s;
        """, [user_id, item_type, item_id])
        return cur.rowcount > 0
    except Exception:
        conn.rollback()
        return False


def get_favorite_movies(user_id):
    try:
        cur.execute("""
            SELECT m.*
            FROM favorites f
            JOIN movies m ON f.item_id = m.movie_id
            WHERE f.user_id=%s AND f.item_type='movie';
        """, [user_id])
        return cur.fetchall()
    except Exception:
        conn.rollback()
        return []

'''
def get_favorite_genres(user_id):
    try:
        cur.execute("""
            SELECT g.*
            FROM favorites f
            JOIN genres g ON f.item_id = g.id
            WHERE f.user_id=%s AND f.item_type='genre';
        """, [user_id])
        return cur.fetchall()
    except Exception:
        conn.rollback()
        return []


def get_favorite_actors(user_id):
    try:
        cur.execute("""
            SELECT p.person_id, p.name
            FROM favorites f
            JOIN persons p ON f.item_id = p.person_id
            WHERE f.user_id=%s AND f.item_type='actor';
        """, [user_id])
        return cur.fetchall()
    except Exception:
        conn.rollback()
        return []
