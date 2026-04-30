# page_favorites.py

from tlbx_imports import *
from ui_toolbox import *
from favoriting import get_favorite_movies, remove_favorite
from db_actions import cur, conn


@ui.page('/favorites')
def favorites_page():

    uit_banner()

    user_id = app.storage.user.get('user_id')

    if not user_id:
        ui.label("You must be logged in to view favorites.").classes("text-red-500 text-xl")
        uit_footnote()
        return

    ui.label("Your Favorite Movies").classes("text-2xl font-bold mb-4")

    favorites = get_favorite_movies(user_id)

    if not favorites:
        ui.label("You have no favorite movies yet.")
        uit_footnote()
        return

    for fav in favorites:
        movie_id = fav['movie_id']

        cur.execute("""
            SELECT movie_id, title, release_date, runtime
            FROM movies
            WHERE movie_id = %s;
        """, [movie_id])
        movie = cur.fetchone()

        if not movie:
            continue

        title = movie['title']
        release = movie['release_date']
        runtime = movie['runtime']

        with ui.card().classes("w-full mb-3"):
            ui.label(f"🎬 {title}").classes("text-lg font-bold")
            ui.label(f"Release Date: {release}")
            ui.label(f"Runtime: {runtime} minutes")

            with ui.row().classes("mt-2"):
                ui.button(
                    "View",
                    on_click=lambda e, movie_id=movie_id: ui.navigate.to(f'/movie/{movie_id}')
                )

                ui.button(
                    "Remove",
                    on_click=lambda e, movie_id=movie_id: (
                        remove_favorite(user_id, movie_id),
                        ui.notify("Removed from favorites"),
                        ui.navigate.to('/favorites')
                    ),
                    color="red"
                )

    uit_footnote()