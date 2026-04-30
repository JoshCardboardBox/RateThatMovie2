from tlbx_imports import *
from ui_toolbox import *
from db_actions import *



# Create a New Account
@ui.page('/create_account')
def create_account():
    uit_banner()

    #check if created account; if not, go to step 1
    create_account_process()

    uit_footnote()

#If you hadn't made an account
def create_account_process():
    #Internal Subfunction to Create account
    def try_create_account():
        #fetch info
        username = security_input(username_box.value)
        email = security_input(email_box.value)
        password = security_input(password_box.value)

        #check if account creation is successful
        #(error messages are given through the called function)
        p = check_accCreate_validity(username, email, password)
        if p == True:
            create_user(username, email, password)
            step1_card.set_visibility(False)
            step2_card.set_visibility(True)

    #User Interface
    #First, ask what info the account should have...
    with ui.card() as step1_card:
        ui.label("Create New Account!")
        username_box = ui.input("Username: ")
        email_box = ui.input("Email: ")
        password_box = ui.input("Password: ")
        ui.button('Sign Up', on_click=try_create_account)

    #Once you make an account, you are given this card
    with ui.card() as step2_card:
        ui.label("You have created this account.")
        ui.label("If you wish to use your account, return home and log in as your account.")
        ui.button('Return Home', on_click=lambda: ui.navigate.to('/'))

    # set card visibility
    step1_card.set_visibility(True)
    step2_card.set_visibility(False)


#Determine if, given the information, we can make or cannot make an account
# True if possible, False if not
def check_accCreate_validity(username, email, password):
    #1st, check if ANY inputs are empty
    if username == "" or email == "" or password == "":
        ui.notify('Fill out all the boxes', color='negative')
        return False

    #2nd, check if ANY inputs are already shared
    ch = check_username_email_matches(username, email)
    if ch == True:
        ui.notify('Error. Please change the typed information.', color='negative')
        return False

    #3rd, make sure the email has a '@'
    if '@' not in email:
        ui.notify('Enter a valid email.', color='negative')
        return False

    #If all tests are passed, return True
    return True
