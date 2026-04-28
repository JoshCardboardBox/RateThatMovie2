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

    s = check_login()
    if s == False:
        homepage_dashboard()

    check_login_msg()
    uit_footnote()

def homepage_dashboard():
    with ui.card().style('align-items: stretch').classes('w-full'):
        ui.label("Dashboard").style('font-size: 125%')
        ui.button('See Reviews', on_click=lambda: ui.navigate.to('/reviews'))
        ui.button('Search Movies, Actors, and More!', on_click=lambda: ui.navigate.to('/search'))
