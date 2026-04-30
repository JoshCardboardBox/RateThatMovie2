from tlbx_imports import *
from ui_toolbox import *


# homepage
@ui.page('/')
def homepage():
    uit_banner()

    with ui.row():
        with ui.card():
            ui.image('RateThatMovieMeme.png').classes('w-128 justify-content: center')
        with ui.card():
            ui.label("Welcome!").style('font-size: 125%')
            ui.label("Hello, fellow movie connoisseur!")
            ui.label("Need to express your love or hatred of any movie?")
            ui.label("Well, this website is for individuals like you.")

    # Optional login message
    check_login_msg()

    # ⭐ Always show dashboard buttons
    homepage_dashboard()

    uit_footnote()

def homepage_dashboard():
    with ui.card().style('align-items: stretch').classes('w-full'):
        ui.label("Dashboard").style('font-size: 125%')
        ui.button('See Reviews', on_click=lambda: ui.navigate.to('/reviews'))
        ui.button('Search Movies, Actors, and More!', on_click=lambda: ui.navigate.to('/search'))
        ui.button("My Favorites", on_click=lambda: ui.navigate.to('/favorites'))
        ui.button('See Your Watchlists', on_click=lambda: ui.navigate.to('/watchlists'))




def check_login_msg():
    s = check_login()
    username = app.storage.user.get('username', None)  # default if not logged in is None
    if s:  # true
        ui.label("Welcome, " + username + ".")
    else:
        ui.label("You are not logged in.")
