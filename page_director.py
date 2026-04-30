from tlbx_imports import *
from ui_toolbox import *
from db_actions import (
    get_director_details,
    get_movies_by_director,
    add_favorite_item,
    remove_favorite_item,
    is_favorited_item,
)


@ui.page('/director/{director_id}')
def director_page(director_id: int):

    uit_banner()

    director = get_director_details(director_id)

    if not director:
        ui.label("Director not found.").classes("text-red-500 text-xl")
        uit_footnote()
        return

    user_id = app.storage.user.get('user_id')

    # ---------------- DIRECTOR HEADER ----------------
    with ui.row().classes("items-center mb-4"):
        ui.label(director['name']).classes("text-3xl font-bold")

        if user_id:
            is_fav = is_favorited_item(user_id, 'director', director_id)

            def toggle_director_fav():
                if is_fav:
                    remove_favorite_item(user_id, 'director', director_id)
                    ui.notify("Removed director from favorites")
                else:
                    add_favorite_item(user_id, 'director', director_id)
                    ui.notify("Added director to favorites")
                ui.navigate.to(f"/director/{director_id}")

            ui.button(
                "❤️ Unfavorite Director" if is_fav else "🤍 Favorite Director",
                on_click=toggle_director_fav,
            ).classes("ml-4")

    # ---------------- MOVIES ----------------
    ui.label("Movies Directed").classes("text-2xl font-bold mt-2")

    movies = get_movies_by_director(director_id)

    if not movies:
        ui.label("No movies found for this director.")
        uit_footnote()
        return

    for m in movies:
        movie_id = m['movie_id']
        title = m['title']
        release = m['release_date']

        with ui.card().classes("w-full mb-3 p-4"):
            ui.label(f"{title} ({release})").classes("text-lg font-bold")

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
                        ui.navigate.to(f"/director/{director_id}")

                    ui.button(
                        "❤️ Unfavorite Movie" if is_movie_fav else "🤍 Favorite Movie",
                        on_click=toggle_movie_fav,
                    )

    uit_footnote()

