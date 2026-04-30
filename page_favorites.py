from tlbx_imports import *
from ui_toolbox import *
from db_actions import (
    get_favorite_movies,
    get_favorite_actors,
    get_favorite_directors,
    remove_favorite_item,
)


@ui.page('/favorites')
def favorites_page():

    uit_banner()

    user_id = app.storage.user.get('user_id')

    if not user_id:
        ui.label("You must be logged in to view favorites.").classes("text-red-500 text-xl")
        uit_footnote()
        return


    # FAVORITE MOVIES

    ui.label("🎬 Your Favorite Movies").classes("text-2xl font-bold mb-4")

    movies = get_favorite_movies(user_id)

    if not movies:
        ui.label("You have no favorite movies yet.").classes("text-gray-500 mb-6")
    else:
        for fav in movies:
            movie_id = fav['movie_id']
            title = fav['title']
            release = fav['release_date']

            with ui.card().classes("w-full mb-3 p-4"):
                ui.label(f"{title}").classes("text-lg font-bold")
                ui.label(f"Release Date: {release}")

                with ui.row().classes("mt-2"):
                    ui.button(
                        "View",
                        on_click=lambda e, mid=movie_id: ui.navigate.to(f"/movie/{mid}")
                    )

                    ui.button(
                        "Remove",
                        color="red",
                        on_click=lambda e, mid=movie_id: (
                            remove_favorite_item(user_id, 'movie', mid),
                            ui.notify("Removed from favorites"),
                            ui.navigate.to('/favorites')
                        )
                    )

    ui.separator()


    # FAVORITE ACTORS

    ui.label("🎭 Your Favorite Actors").classes("text-2xl font-bold mt-6 mb-4")

    actors = get_favorite_actors(user_id)

    if not actors:
        ui.label("You have no favorite actors yet.").classes("text-gray-500 mb-6")
    else:
        for fav in actors:
            person_id = fav['person_id']
            name = fav['name']

            with ui.card().classes("w-full mb-3 p-4"):
                ui.label(name).classes("text-lg font-bold")

                with ui.row().classes("mt-2"):
                    ui.button(
                        "View Actor",
                        on_click=lambda e, pid=person_id: ui.navigate.to(f"/actor/{pid}")
                    )

                    ui.button(
                        "Remove",
                        color="red",
                        on_click=lambda e, pid=person_id: (
                            remove_favorite_item(user_id, 'actor', pid),
                            ui.notify("Removed from favorites"),
                            ui.navigate.to('/favorites')
                        )
                    )

    ui.separator()


    # FAVORITE DIRECTORS

    ui.label("🎬 Your Favorite Directors").classes("text-2xl font-bold mt-6 mb-4")

    directors = get_favorite_directors(user_id)

    if not directors:
        ui.label("You have no favorite directors yet.").classes("text-gray-500 mb-6")
    else:
        for fav in directors:
            director_id = fav['director_id']
            name = fav['name']

            with ui.card().classes("w-full mb-3 p-4"):
                ui.label(name).classes("text-lg font-bold")

                with ui.row().classes("mt-2"):
                    ui.button(
                        "View Director",
                        on_click=lambda e, did=director_id: ui.navigate.to(f"/director/{did}")
                    )

                    ui.button(
                        "Remove",
                        color="red",
                        on_click=lambda e, did=director_id: (
                            remove_favorite_item(user_id, 'director', did),
                            ui.notify("Removed from favorites"),
                            ui.navigate.to('/favorites')
                        )
                    )

    uit_footnote()