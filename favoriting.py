# favoriting.py

from tlbx_imports import *
from db_actions import cur, conn



# ADD FAVORITE (MOVIES ONLY)

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



# REMOVE FAVORITE

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



# CHECK IF FAVORITED

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



# GET ALL FAVORITE MOVIES FOR A USER

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