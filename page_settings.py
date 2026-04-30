from tlbx_imports import *
from ui_toolbox import *
from db_actions import *

#coded w/ assistance from ChatGPT (not much tho)


@ui.page('/settings')
def settings():
    uit_banner()

    #Deny access to not logged-in users
    s = check_login()
    if s:
        __settings_body()
    else:
        ui.label('You are not logged in.').style('color: red')
        ui.button("Return Home", on_click=lambda: ui.navigate.to('/'))

    uit_footnote()



def __settings_body():
    user_id = app.storage.user.get('user_id', None)

    with ui.card():
        ui.label("Settings").style('font-size: 200%')
        ui.label(f"Your user id is: {user_id}")

        ui.space()

        __section_updateuserinfo(user_id)  #updating username, email, password

        ui.space()

        __section_deleteuser(user_id)       #deleting the user from the site

        ui.space()

        ui.label('More...')










'''
FUNCTIONS TO UPDATE xxx
'''
@ui.refreshable
def __section_updateuserinfo(user_id):
    user_username = get_user_username(user_id)
    user_email = get_user_email(user_id)
    user_password = get_user_password(user_id)

    ui.label("Change Username, Email, or Password").style('font-size: 140%')
    with ui.grid(rows=3, columns=3):
        ui.label(user_username).style('font-size: 100%; border: 1px solid silver; padding: 6px; border-radius: 10px')
        new_username_box = ui.input('New Username:').props('dense')
        ui.button('Update Username', on_click=lambda: __try_update_username(new_username_box))

        ui.label(user_email).style('font-size: 100%; border: 1px solid silver; padding: 6px; border-radius: 10px')
        new_email_box = ui.input('New Email:').props('dense')
        ui.button('Update Email', on_click=lambda: __try_update_email(new_email_box))

        ui.label(user_password).style('font-size: 100%; border: 1px solid silver; padding: 6px; border-radius: 10px')
        new_password_box = ui.input('New Password:').props('dense')
        ui.button('Update Password', on_click=lambda: __try_update_password(new_password_box))


# Functions to update username
def __try_update_username(new_username_box):
    new_username = security_input(new_username_box.value)   #input validation

    cur.execute("SELECT count(*) FROM users WHERE username=%s", [new_username])
    s = cur.fetchone()['count']

    #check if username is already shared w/ someone else
    if s != 0:
        ui.notify("Please enter a different username", color='negative')
    else:
        user_id = app.storage.user.get('user_id', None)
        cur.execute("UPDATE users SET username=%s WHERE user_id=%s", [new_username, user_id])
        conn.commit()

        ui.notify("Username Updated", color='positive')
        __section_updateuserinfo.refresh(user_id)


def __try_update_email(new_email_box):
    new_email = security_input(new_email_box.value)         #input validation

    cur.execute("SELECT count(*) FROM users WHERE email=%s", [new_email])
    s = cur.fetchone()['count']

    #check if email is already shared w/ someone else
    if s != 0:
        ui.notify("Please enter a different email", color='negative')
    #check if email does not have the '@'
    elif '@' not in new_email:
        ui.notify("Please enter a valid email address", color='negative')
    else:
        user_id = app.storage.user.get('user_id', None)
        cur.execute("UPDATE users SET email=%s WHERE user_id=%s", [new_email, user_id])
        conn.commit()

        ui.notify("Email Updated", color='positive')
        __section_updateuserinfo.refresh(user_id)


def __try_update_password(new_password_box):
    new_password = security_input(new_password_box.value)   #input validation

    user_id = app.storage.user.get('user_id', None)
    cur.execute("UPDATE users SET password=%s WHERE user_id=%s", [new_password, user_id])
    conn.commit()

    ui.notify("Password Updated", color='positive')
    __section_updateuserinfo.refresh(user_id)


'''
FUNCTIONS TO DELETE USER
'''
def __section_deleteuser(user_id):
    def delete_user():
        #first, log the user out
        app.storage.user.pop('user_id')
        app.storage.user.pop('username')

        #delete user data
        cur.execute("DELETE FROM users WHERE user_id=%s", [user_id])
        conn.commit()

        #redirect to home
        ui.notify("User Deleted", color='negative')
        ui.navigate.to('/')

    with ui.dialog() as d, ui.card():
        ui.label("Are you sure you want to delete your account?")
        with ui.row().classes('w-full justify-between'):
            ui.button('🗑️Yes', on_click=lambda: delete_user()).props('color=red').style('width: 7vw')
            ui.space()
            ui.button('No', on_click=d.close).style('width: 7vw')

    ui.label("Delete User Account").style('font-size: 140%')
    ui.button('🗑️ Delete', on_click=d.open).props('color=red')






