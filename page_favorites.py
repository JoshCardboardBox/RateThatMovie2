from tlbx_imports import *
from ui_toolbox import *
from favoriting import (
    get_favorite_movies,
    get_favorite_genres,
    get_favorite_actors
)

@ui.page('/favorites')
def favorites_page():

    uit_banner()

    # ⭐ Correct way to get logged-in user
    user_id = app.storage.user.get('user_id')

    if not user_id:
        ui.label("You must be logged in to view favorites.")
        uit_footnote()
        return

    ui.label("Your Favorites").classes("text-2xl font-bold mt-4")

    # Favorite Movies
    movies = get_favorite_movies(user_id)
    ui.label("Favorite Movies").classes("text-xl mt-4")
    for m in movies:
        ui.label(f"🎬 {m['title']}")

    # Favorite Genres
    genres = get_favorite_genres(user_id)
    ui.label("Favorite Genres").classes("text-xl mt-4")
    for g in genres:
        ui.label(f"🏷️ {g['name']}")

    # Favorite Actors
    actors = get_favorite_actors(user_id)
    ui.label("Favorite Actors").classes("text-xl mt-4")
    for a in actors:
        ui.label(f"⭐ {a['name']}")

    uit_footnote()