from tlbx_imports import *
from ui_toolbox import *
from db_actions import *


password = ""



#login/logout Page
@ui.page('/login')
def login():
    uit_banner()

    #check if logged in, and display different cards based off that.
    s = check_login()
    if s:
        is_logged_in()
    else:
        is_not_logged_in()

    uit_footnote()




#NOT LOGGED IN & LOGGING IN
def is_not_logged_in():
    #Subfunction to log in
    def try_login():
        # check if you can get user with email and password
        email = security_input(email_box.value)
        password = security_input(password_box.value)
        user_id = get_user_id(email, password)
        # if so, store user's info (id & username)
        if user_id != None:
            app.storage.user['user_id'] = user_id
            app.storage.user['username'] = get_user_username(user_id)
            ui.navigate.to('/')  # go home
        # if user does not exist OR is wrong password...
        else:
            ui.notify('Wrong email or password', color='negative')

    #First, ask user to log in
    with ui.card():
        ui.label("Log in through here!")
        email_box = ui.input("Email: ")
        password_box = ui.input("Password: ", password=True, password_toggle_button=True)
        ui.button('Log In', on_click=try_login)


#LOGGING IN & LOGGING OUT (FROM BEING LOGGED IN)
def is_logged_in():
    #Subfunction to log out
    def try_logout():
        # POP STORED INFO
        app.storage.user.pop('user_id')
        app.storage.user.pop('username')

        #Go Home
        ui.notify('You are now logged out', color='positive')
        ui.navigate.to('/')

    #First, page to ask user if they want to log out
    with ui.card():
        ui.label("Click here to log out.")
        ui.button('Log Out', on_click=try_logout)




