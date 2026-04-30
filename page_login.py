from tlbx_imports import *
from ui_toolbox import *
from db_actions import *


password = ""


# LOGIN / LOGOUT PAGE
@ui.page('/login')
def login():
    uit_banner()

    # Check if logged in
    if check_login():
        is_logged_in()
    else:
        is_not_logged_in()

    uit_footnote()



# NOT LOGGED IN — SHOW LOGIN FORM
def is_not_logged_in():

    def try_login():
        email = security_input(email_box.value)
        password = security_input(password_box.value)

        # Check credentials
        user_id = get_user_id(email, password)

        if user_id is not None:
            # ⭐ Store user info globally (NiceGUI session storage)
            app.storage.user['user_id'] = user_id
            app.storage.user['username'] = get_user_username(user_id)

            ui.notify('Login successful!', color='positive')
            ui.navigate.to('/')  # Go home
        else:
            ui.notify('Wrong email or password', color='negative')

    # Login card UI
    with ui.card():
        ui.label("Log in through here!")
        email_box = ui.input("Email: ")
        password_box = ui.input("Password: ", password=True, password_toggle_button=True)
        ui.button('Log In', on_click=try_login)



# LOGGED IN — SHOW LOGOUT OPTION
def is_logged_in():

    def try_logout():
        # Remove stored session info
        app.storage.user.pop('user_id', None)
        app.storage.user.pop('username', None)

        ui.notify('You are now logged out', color='positive')
        ui.navigate.to('/')

    # Logout card UI
    with ui.card():
        ui.label("Click here to log out.")
        ui.button('Log Out', on_click=try_logout)



