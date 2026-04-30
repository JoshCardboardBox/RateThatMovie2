# page_movie.py

from tlbx_imports import *
from ui_toolbox import *
from db_actions import get_movie_details
from favoriting import add_favorite, remove_favorite, is_favorited


@ui.page('/movie/{movie_id}')
def movie_page(movie_id: int):

    uit_banner()

    # Fetch movie details
    movie = get_movie_details(movie_id)

    if not movie:
        ui.label("Movie not found.").classes("text-red-500 text-xl")
        uit_footnote()
        return

    # Extract fields from dict row
    title = movie['title']
    runtime = movie['runtime']
    release = movie['release_date']
    budget = movie['budget']
    revenue = movie['revenue']
    status = movie['status']
    adult = movie['adult']
    genres = movie['genres']
    language = movie['original_language']

    # Movie header
    ui.label(title).classes("text-3xl font-bold mb-2")
    ui.label(f"Release Date: {release}")
    ui.label(f"Runtime: {runtime} minutes")
    ui.label(f"Budget: ${budget:,}")
    ui.label(f"Revenue: ${revenue:,}")
    ui.label(f"Status: {status}")
    ui.label(f"Adult: {'Yes' if adult else 'No'}")
    ui.label(f"Genres: {genres}")
    ui.label(f"Original Language: {language}")

    ui.separator()

    # ---------------------------------------------------------
    # FAVORITING BUTTON (MOVIES ONLY)
    # ---------------------------------------------------------
    user_id = app.storage.user.get('user_id')

    if not user_id:
        ui.label("Log in to favorite movies.").classes("text-red-500 mt-4")
        uit_footnote()
        return

    # Check if already favorited
    favorited = is_favorited(user_id, movie_id)

    def toggle_favorite():
        if is_favorited(user_id, movie_id):
            remove_favorite(user_id, movie_id)
            ui.notify("Removed from favorites")
        else:
            add_favorite(user_id, movie_id)
            ui.notify("Added to favorites")

        # Refresh page
        ui.navigate.to(f'/movie/{movie_id}')

    ui.button(
        "❤️ Remove from Favorites" if favorited else "🤍 Add to Favorites",
        on_click=toggle_favorite
    ).classes("mt-4")

    uit_footnote()