# page_actor.py

from tlbx_imports import *
from ui_toolbox import *
from db_actions import get_actor_details, get_movies_by_actor
from favoriting import add_favorite, remove_favorite, is_favorited


@ui.page('/actor/{person_id}')
def actor_page(person_id: int):

    uit_banner()

    actor = get_actor_details(person_id)

    if not actor:
        ui.label("Actor not found.").classes("text-red-500 text-xl")
        uit_footnote()
        return

    ui.label(actor['name']).classes("text-3xl font-bold mb-4")

    ui.label("Movies").classes("text-2xl font-bold mt-4")

    movies = get_movies_by_actor(person_id)

    if not movies:
        ui.label("No movies found for this actor.")
        uit_footnote()
        return

    user_id = app.storage.user.get('user_id')

    for m in movies:
        movie_id = m['movie_id']
        title = m['title']
        release = m['release_date']
        character = m['character']

        with ui.card().classes("w-full mb-3 p-4"):
            ui.label(f"{title} ({release}) — {character}").classes("text-lg font-bold")

            with ui.row().classes("mt-2"):
                ui.button(
                    "View",
                    on_click=lambda e, id=movie_id: ui.navigate.to(f"/movie/{id}")
                )

                if user_id:
                    fav = is_favorited(user_id, movie_id)

                    def toggle_fav(movie_id=movie_id):
                        if is_favorited(user_id, movie_id):
                            remove_favorite(user_id, movie_id)
                            ui.notify("Removed from favorites")
                        else:
                            add_favorite(user_id, movie_id)
                            ui.notify("Added to favorites")
                        ui.navigate.to(f"/actor/{person_id}")

                    ui.button(
                        "❤️ Remove" if fav else "🤍 Add",
                        on_click=toggle_fav
                    )

    uit_footnote()