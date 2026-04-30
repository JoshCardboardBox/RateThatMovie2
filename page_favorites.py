from tlbx_imports import *
from ui_toolbox import *
from db_actions import (
    get_favorite_movies,
    get_favorite_actors,
    get_favorite_directors,
)


@ui.page('/favorites')
def favorites_page():

    uit_banner()

    user_id = app.storage.user.get('user_id')

    if not user_id:
        ui.label("You must be logged in to view favorites.").classes("text-red-500 text-xl")
        uit_footnote()
        return

    ui.label("My Favorites").classes("text-4xl font-bold mb-6")

    # ---------------------------------------------------------
    # ⭐ FAVORITE MOVIES
    # ---------------------------------------------------------
    ui.label("Favorite Movies").classes("text-2xl font-bold mt-4 mb-2")

    movies = get_favorite_movies(user_id)

    if not movies:
        ui.label("You have no favorite movies yet.").classes("text-gray-500 mb-4")
    else:
        for m in movies:
            movie_id = m['movie_id']
            title = m['title']
            release = m['release_date']

            with ui.card().classes("w-full mb-3 p-4"):
                ui.label(f"{title} ({release})").classes("text-lg font-bold")

                ui.button(
                    "View Movie",
                    on_click=lambda e, id=movie_id: ui.navigate.to(f"/movie/{id}")
                ).classes("mt-2")


    # ---------------------------------------------------------
    # ⭐ FAVORITE ACTORS
    # ---------------------------------------------------------
    ui.label("Favorite Actors").classes("text-2xl font-bold mt-8 mb-2")

    actors = get_favorite_actors(user_id)

    if not actors:
        ui.label("You have no favorite actors yet.").classes("text-gray-500 mb-4")
    else:
        for a in actors:
            person_id = a['person_id']
            name = a['name']

            with ui.card().classes("w-full mb-3 p-4"):
                ui.label(name).classes("text-lg font-bold")

                ui.button(
                    "View Actor",
                    on_click=lambda e, id=person_id: ui.navigate.to(f"/actor/{id}")
                ).classes("mt-2")


    # ---------------------------------------------------------
    # ⭐ FAVORITE DIRECTORS
    # ---------------------------------------------------------
    ui.label("Favorite Directors").classes("text-2xl font-bold mt-8 mb-2")

    directors = get_favorite_directors(user_id)

    if not directors:
        ui.label("You have no favorite directors yet.").classes("text-gray-500 mb-4")
    else:
        for d in directors:
            director_id = d['director_id']
            name = d['name']

            with ui.card().classes("w-full mb-3 p-4"):
                ui.label(name).classes("text-lg font-bold")

                ui.button(
                    "View Director",
                    on_click=lambda e, id=director_id: ui.navigate.to(f"/director/{id}")
                ).classes("mt-2")

    uit_footnote()