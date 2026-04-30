from tlbx_imports import *
from ui_toolbox import *
from db_actions import (
    get_movie_details,
    get_full_cast,
    get_full_crew,
    add_favorite_item,
    remove_favorite_item,
    is_favorited_item,
)
from rating_tool import star_rating


@ui.page('/movie/{movie_id}')
def movie_page(movie_id: int):

    uit_banner()

    movie = get_movie_details(movie_id)

    if not movie:
        ui.label("Movie not found.").classes("text-red-500 text-xl")
        uit_footnote()
        return

    # Extract fields
    title = movie['title']
    runtime = movie['runtime']
    release = movie['release_date']
    budget = movie['budget']
    revenue = movie['revenue']
    status = movie['status']
    adult = movie['adult']
    genres = movie['genres']
    language = movie['original_language']

    # Header
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


    # USER ID + RATING

    user_id = app.storage.user.get('user_id')

    if user_id:
        star_rating(user_id, 'movie', movie_id)
    else:
        ui.label("Log in to rate and favorite movies.").classes("text-red-500 mt-4")
        uit_footnote()
        return


    # FAVORITING

    favorited = is_favorited_item(user_id, 'movie', movie_id)

    def toggle_favorite():
        if favorited:
            remove_favorite_item(user_id, 'movie', movie_id)
            ui.notify("Removed from favorites")
        else:
            add_favorite_item(user_id, 'movie', movie_id)
            ui.notify("Added to favorites")

        ui.navigate.to(f"/movie/{movie_id}")

    ui.button(
        "❤️ Remove from Favorites" if favorited else "🤍 Add to Favorites",
        on_click=toggle_favorite
    ).classes("mt-4")

    ui.separator()


    # CAST SECTION

    ui.label("Cast").classes("text-2xl font-bold mt-6 mb-2")

    cast = get_full_cast(movie_id)

    if not cast:
        ui.label("No cast information available.").classes("text-gray-500")
    else:
        for c in cast:
            with ui.card().classes("w-full mb-3 p-4"):
                ui.label(f"{c['name']} as {c['character']}").classes("text-lg font-bold")
                ui.button(
                    "View Actor",
                    on_click=lambda e, pid=c['person_id']: ui.navigate.to(f"/actor/{pid}")
                )

    ui.separator()


    # CREW SECTION

    ui.label("Crew").classes("text-2xl font-bold mt-6 mb-2")

    crew = get_full_crew(movie_id)

    if not crew:
        ui.label("No crew information available.").classes("text-gray-500")
    else:
        for c in crew:
            with ui.card().classes("w-full mb-3 p-4"):
                ui.label(f"{c['name']} — {c['job']} ({c['department']})").classes("text-lg font-bold")

                # Directors go to director page, others to actor page
                def go_to_person(pid=c['person_id'], job=c['job']):
                    if job.lower() == "director":
                        ui.navigate.to(f"/director/{pid}")
                    else:
                        ui.navigate.to(f"/actor/{pid}")

                ui.button("View Person", on_click=go_to_person)

    uit_footnote()