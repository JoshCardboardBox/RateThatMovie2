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


@ui.page('/movie/{movie_id}')
def movie_page(movie_id: int):

    uit_banner()

    movie = get_movie_details(movie_id)

    if not movie:
        ui.label("Movie not found.").classes("text-red-500 text-xl")
        uit_footnote()
        return

    user_id = app.storage.user.get('user_id')

    # ---------------- MOVIE HEADER ----------------
    with ui.row().classes("items-center mb-4"):
        ui.label(movie['title']).classes("text-4xl font-bold")

        if user_id:
            is_fav = is_favorited_item(user_id, 'movie', movie_id)

            def toggle_movie_fav():
                if is_fav:
                    remove_favorite_item(user_id, 'movie', movie_id)
                    ui.notify("Removed movie from favorites")
                else:
                    add_favorite_item(user_id, 'movie', movie_id)
                    ui.notify("Added movie to favorites")
                ui.navigate.to(f"/movie/{movie_id}")

            ui.button(
                "❤️ Unfavorite Movie" if is_fav else "🤍 Favorite Movie",
                on_click=toggle_movie_fav,
            ).classes("ml-4")

    # ---------------- MOVIE DETAILS ----------------
    ui.label(f"Release Date: {movie['release_date']}").classes("text-lg")
    ui.label(f"Runtime: {movie['runtime']} minutes").classes("text-lg")
    ui.label(f"Genres: {movie['genres']}").classes("text-lg")

    # Additional details restored:
    ui.label(f"Budget: ${movie['budget']:,}" if movie['budget'] else "Budget: N/A").classes("text-lg")
    ui.label(f"Revenue: ${movie['revenue']:,}" if movie['revenue'] else "Revenue: N/A").classes("text-lg")
    ui.label(f"Status: {movie['status']}").classes("text-lg")
    ui.label(f"Original Language: {movie['original_language']}").classes("text-lg")
    ui.label(f"Adult: {'Yes' if movie['adult'] else 'No'}").classes("text-lg mb-6")

    # ---------------- CAST SECTION ----------------
    ui.label("Cast").classes("text-3xl font-bold mt-6 mb-2")

    cast = get_full_cast(movie_id)

    if not cast:
        ui.label("No cast information available.").classes("text-gray-500")
    else:
        for c in cast:
            person_id = c['person_id']
            name = c['name']
            character = c['character']

            with ui.card().classes("w-full mb-3 p-4"):
                ui.label(f"{name} as {character}").classes("text-lg font-bold")

                with ui.row().classes("mt-2"):
                    ui.button(
                        "View Actor",
                        on_click=lambda e, id=person_id: ui.navigate.to(f"/actor/{id}")
                    )

                    if user_id:
                        is_fav_actor = is_favorited_item(user_id, 'actor', person_id)

                        def toggle_actor_fav(pid=person_id):
                            if is_favorited_item(user_id, 'actor', pid):
                                remove_favorite_item(user_id, 'actor', pid)
                                ui.notify("Removed actor from favorites")
                            else:
                                add_favorite_item(user_id, 'actor', pid)
                                ui.notify("Added actor to favorites")
                            ui.navigate.to(f"/movie/{movie_id}")

                        ui.button(
                            "❤️ Unfavorite Actor" if is_fav_actor else "🤍 Favorite Actor",
                            on_click=toggle_actor_fav,
                        )

    # ---------------- CREW SECTION ----------------
    ui.label("Crew").classes("text-3xl font-bold mt-8 mb-2")

    crew = get_full_crew(movie_id)

    if not crew:
        ui.label("No crew information available.").classes("text-gray-500")
    else:
        for c in crew:
            person_id = c['person_id']
            name = c['name']
            job = c['job']
            dept = c['department']

            with ui.card().classes("w-full mb-3 p-4"):
                ui.label(f"{name} — {job} ({dept})").classes("text-lg font-bold")

                with ui.row().classes("mt-2"):
                    # Directors go to director page, everyone else to actor page
                    ui.button(
                        "View Person",
                        on_click=lambda e, id=person_id, j=job: (
                            ui.navigate.to(f"/director/{id}") if j.lower() == "director"
                            else ui.navigate.to(f"/actor/{id}")
                        )
                    )

                    if user_id:
                        item_type = 'director' if job.lower() == 'director' else 'actor'
                        is_fav_person = is_favorited_item(user_id, item_type, person_id)

                        def toggle_person_fav(pid=person_id, it=item_type):
                            if is_favorited_item(user_id, it, pid):
                                remove_favorite_item(user_id, it, pid)
                                ui.notify("Removed from favorites")
                            else:
                                add_favorite_item(user_id, it, pid)
                                ui.notify("Added to favorites")
                            ui.navigate.to(f"/movie/{movie_id}")

                        ui.button(
                            "❤️ Unfavorite" if is_fav_person else "🤍 Favorite",
                            on_click=toggle_person_fav,
                        )

    uit_footnote()