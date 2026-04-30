from tlbx_imports import *
from ui_toolbox import *
from db_actions import get_director_details, get_movies_by_director
from favoriting import add_favorite, remove_favorite, is_favorited
from rating_tool import star_rating

@ui.page('/director/{director_id}')
def director_page(director_id: int):

    uit_banner()

    director = get_director_details(director_id)

    if not director:
        ui.label("Director not found.").classes("text-red-500 text-xl")
        uit_footnote()
        return

    ui.label(director['name']).classes("text-3xl font-bold mb-4")

    ui.label("Movies Directed").classes("text-2xl font-bold mt-4")

    movies = get_movies_by_director(director_id)

    if not movies:
        ui.label("No movies found for this director.")
        uit_footnote()
        return

    user_id = app.storage.user.get('user_id')
    if user_id:
        star_rating(user_id, 'director', director_id)

    for m in movies:
        movie_id = m['movie_id']
        title = m['title']
        release = m['release_date']

        with ui.card().classes("w-full mb-3 p-4"):
            ui.label(f"{title} ({release})").classes("text-lg font-bold")

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
                        ui.navigate.to(f"/director/{director_id}")

                    ui.button(
                        "❤️ Remove" if fav else "🤍 Add",
                        on_click=toggle_fav
                    )

    uit_footnote()