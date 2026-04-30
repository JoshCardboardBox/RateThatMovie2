from tlbx_imports import *
from ui_toolbox import *
from db_actions import (
    search_movies,
    search_actors,
    search_directors,
)


@ui.page('/search')
def search_page():

    uit_banner()

    ui.label("Search").classes("text-3xl font-bold mb-4")

    query = ui.input("Search for movies, actors, or directors").classes("w-full")

    results_container = ui.column().classes("mt-4")

    tabs = ui.tabs().classes("mt-4")
    with tabs:
        movie_tab = ui.tab("Movies")
        actor_tab = ui.tab("Actors")
        director_tab = ui.tab("Directors")

    with ui.tab_panels(tabs, value=movie_tab):

        # ---------------- MOVIES ----------------
        with ui.tab_panel(movie_tab):

            def do_movie_search():
                results_container.clear()
                if not query.value:
                    return

                results = search_movies(query.value)

                with results_container:
                    if not results:
                        ui.label("No movies found.")
                        return

                    for m in results:
                        ui.button(
                            f"{m['title']} ({m['release_date']})",
                            on_click=lambda e, id=m['movie_id']: ui.navigate.to(f"/movie/{id}")
                        ).classes("w-full mb-2")

            ui.button("Search Movies", on_click=do_movie_search).classes("mt-2")

        # ---------------- ACTORS ----------------
        with ui.tab_panel(actor_tab):

            def do_actor_search():
                results_container.clear()
                if not query.value:
                    return

                results = search_actors(query.value)

                with results_container:
                    if not results:
                        ui.label("No actors found.")
                        return

                    for a in results:
                        ui.button(
                            a['name'],
                            on_click=lambda e, id=a['person_id']: ui.navigate.to(f"/actor/{id}")
                        ).classes("w-full mb-2")

            ui.button("Search Actors", on_click=do_actor_search).classes("mt-2")

        # ---------------- DIRECTORS ----------------
        with ui.tab_panel(director_tab):

            def do_director_search():
                results_container.clear()
                if not query.value:
                    return

                results = search_directors(query.value)

                with results_container:
                    if not results:
                        ui.label("No directors found.")
                        return

                    for d in results:
                        ui.button(
                            d['name'],
                            on_click=lambda e, id=d['director_id']: ui.navigate.to(f"/director/{id}")
                        ).classes("w-full mb-2")

            ui.button("Search Directors", on_click=do_director_search).classes("mt-2")

    uit_footnote()