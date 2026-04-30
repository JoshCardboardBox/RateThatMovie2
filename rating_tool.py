from nicegui import ui
from db_actions import set_rating_item, get_rating_item, get_average_rating

def star_rating(user_id, item_type, item_id):

    container = ui.column()

    user_rating = get_rating_item(user_id, item_type, item_id)
    avg_rating = get_average_rating(item_type, item_id)

    def render():
        container.clear()

        # ---------------- USER RATING ----------------
        with container:
            ui.label("Your Rating:").classes("text-xl font-bold")

            with ui.row().classes("items-center gap-2"):
                for i in range(1, 6):
                    star = "★" if user_rating and i <= user_rating else "☆"

                    def set_rating(r=i):
                        nonlocal user_rating
                        set_rating_item(user_id, item_type, item_id, r)
                        user_rating = r
                        render()

                    ui.button(star, on_click=set_rating).classes("text-3xl")

        # ---------------- AVERAGE RATING ----------------
        with container:
            ui.label("Average Rating:").classes("text-xl font-bold mt-4")

            if avg_rating:
                filled = int(round(avg_rating))

                with ui.row().classes("items-center gap-2"):
                    for i in range(1, 6):
                        star = "★" if i <= filled else "☆"
                        ui.label(star).classes("text-3xl")

                ui.label(f"{avg_rating:.2f} / 5").classes("text-lg text-gray-500")

            else:
                ui.label("No ratings yet.").classes("text-gray-500")

    render()