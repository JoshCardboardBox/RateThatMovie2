from tlbx_imports import *
from ui_toolbox import *
from db_actions import (
    get_actor_details,
    get_movies_by_actor,
    add_favorite_item,
    remove_favorite_item,
    is_favorited_item,
)


@ui.page('/actor/{person_id}')
def actor_page(person_id: int):

    uit_banner()

    actor = get_actor_details(person_id)

    if not actor:
        ui.label("Actor not found.").classes("text-red-500 text-xl")
        uit_footnote()
        return

    user_id = app.storage.user.get('user_id')

    # ---------------- ACTOR HEADER ----------------
    with ui.row().classes("items-center mb-4"):
        ui.label(actor['name']).classes("text-3xl font-bold")

        if user_id:
            is_fav = is_favorited_item(user_id, 'actor', person_id)

            def toggle_actor_fav():
                if is_fav:
                    remove_favorite_item(user_id, 'actor', person_id)
                    ui.notify("Removed actor from favorites")
                else:
                    add_favorite_item(user_id, 'actor', person_id)
                    ui.notify("Added actor to favorites")
                ui.navigate.to(f"/actor/{person_id}")

            ui.button(
                "❤️ Unfavorite Actor" if is_fav else "🤍 Favorite Actor",
                on_click=toggle_actor_fav,
            ).classes("ml-4")

    # ---------------- MOVIES ----------------
    ui.label("Movies").classes("text-2xl font-bold mt-2")

    movies = get_movies_by_actor(person_id)

    if not movies:
        ui.label("No movies found for this actor.")
        uit_footnote()
        return

    for m in movies:
        movie_id = m['movie_id']
        title = m['title']
        release = m['release_date']
        character = m['character']

        with ui.card().classes("w-full mb-3 p-4"):
            ui.label(f"{title} ({release}) — {character}").classes("text-lg font-bold")

            with ui.row().classes("mt-2"):
                ui.button(
                    "View Movie",
                    on_click=lambda e, id=movie_id: ui.navigate.to(f"/movie/{id}")
                )

                if user_id:
                    is_movie_fav = is_favorited_item(user_id, 'movie', movie_id)

                    def toggle_movie_fav(mid=movie_id):
                        if is_favorited_item(user_id, 'movie', mid):
                            remove_favorite_item(user_id, 'movie', mid)
                            ui.notify("Removed movie from favorites")
                        else:
                            add_favorite_item(user_id, 'movie', mid)
                            ui.notify("Added movie to favorites")
                        ui.navigate.to(f"/actor/{person_id}")

                    ui.button(
                        "❤️ Unfavorite Movie" if is_movie_fav else "🤍 Favorite Movie",
                        on_click=toggle_movie_fav,
                    )

    uit_footnote()