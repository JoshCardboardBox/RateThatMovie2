from tlbx_imports import *
from ui_toolbox import *
from db_actions import *

#coded w/ assistance from ChatGPT (not much tho)

@ui.page('/watchlists')
def watchlist():
    uit_banner()

    # Deny access to not logged-in users
    s = check_login()
    if s:
        __watchlists_body()
    else:
        ui.label('You are not logged in.').style('color: red')
        ui.button("Return Home", on_click=lambda: ui.navigate.to('/'))

    uit_footnote()


def __watchlists_body():
    with ui.card() as view_opts:
        ui.label("Watchlists").style('font-size: 200%')
        ui.label("This is where users can assemble lists of movies they want to watch.")

        ui.space()

        ui.label("What do you want to do?")
        with ui.row():
            ui.button('Modify Lists', on_click=lambda: ui.navigate.to('/watchlists_modify'))
            ui.space()
            ui.button('Create List', on_click=lambda: ui.navigate.to('/watchlists_create'))
            ui.space()
            ui.button('Delete List', on_click=lambda: ui.navigate.to('/watchlists_delete')).props('color=red')

    ui.space()

    with ui.card() as view_card:
        ui.label("Here are your watchlists...")
        __watchlists_view()

# show all watchlists the user has made...
def __watchlists_view():
    user_id = app.storage.user.get('user_id', None)

    cur.execute("SELECT * FROM watchlists WHERE user_id=%s", [user_id])
    watchlists = cur.fetchall()  # all watchlists

    for watchlist in watchlists:
        #Create a watchlist card for each watchlist, each containing its items
        with ui.card():
            wl_id = watchlist['list_id']
            wl_name = watchlist['list_name']

            cur.execute("SELECT * FROM watchlist_items as a JOIN movies as b " +
                        "ON a.movie_id = b.movie_id " +
                        "WHERE list_id=%s ORDER BY add_date DESC", [wl_id])
            wl_items = cur.fetchall()

            c = [{'name': 'title', 'field': 'title', 'label': "title"},
                 {'name': 'release_date', 'field': 'release_date', 'label': "release_date"},
                 {'name': 'runtime', 'field': 'runtime', 'label': "runtime"},
                 {'name': 'genres', 'field': 'genres', 'label': "genres"},
                 {'name': 'adult', 'field': 'adult', 'label': "adult"},
                 {'name': 'budget', 'field': 'budget', 'label': "budget"},
                 {'name': 'revenue', 'field': 'revenue', 'label': "revenue"},
                 {'name': 'movie_id', 'field': 'movie_id', 'label': "movie_id"},
                 {'name': 'add_date', 'field': 'add_date', 'label': "add_date"}]

            ui.label(f"Watchlist: {wl_name}, id: {wl_id}").style('font-size: 140%')
            ui.table(columns=c, rows=wl_items).props('flat bordered').style('width: 70vw')

    #Something to show if you have no watchlists.
    if len(watchlists) == 0:
        ui.label('You have not made any watchlists.').style('color: red')






@ui.page('/watchlists_create')
def __watchlists_create():
    uit_banner()

    # Deny access to not logged-in users
    s = check_login()
    if s:
        __watchlists_create_body()
    else:
        ui.label('You are not logged in.').style('color: red')
        ui.button("Return Home", on_click=lambda: ui.navigate.to('/'))

    uit_footnote()

def __watchlists_create_body():
    def __try_wl_create():
        wlc = security_input(wlc_box.value)
        #check if wlc

        cur.execute("SELECT count(*) FROM watchlists WHERE list_name=%s AND user_id=%s", [wlc, user_id])
        s = cur.fetchone()['count']
        if s != 0:
            ui.notify('Watchlist already exists', color='negative')
        else:
            #1st, generate a new id
            unique_id_found = False
            nwl_id = 0
            while(not unique_id_found):
                nwl_id = random.randint(1, 1000000)
                cur.execute("SELECT count(*) FROM watchlists WHERE list_id=%s", [nwl_id])
                matches = cur.fetchone()['count'] #get dictionary, then take int out of dictionary type
                #if you've found a user_id number that no account uses, then continue on...
                if matches == 0:
                    unique_id_found = True


            cur.execute("INSERT INTO watchlists (list_id, list_name, user_id, creation_date) "+
                        "VALUES (%s, %s, %s, (SELECT CURRENT_TIMESTAMP))",
                        [nwl_id, wlc, user_id])
            conn.commit()
            part1.set_visibility(False)
            part2.set_visibility(True)

            ui.notify('Watchlist created.', color='positive')


    user_id = app.storage.user.get('user_id', None)

    with ui.card() as part1:
        ui.label("Create Watchlist").style('font-size: 200%')

        with ui.row():
            wlc_box = ui.input("Enter Name")
            ui.button('Create!', on_click=lambda: __try_wl_create())

    with ui.card() as part2:
        ui.label("You've created a watchlist")
        ui.button("Go Home", on_click=lambda: ui.navigate.to('/'))

    part1.set_visibility(True)
    part2.set_visibility(False)



@ui.page('/watchlists_modify')
def __watchlists_modify():
    uit_banner()

    # Deny access to not logged-in users
    s = check_login()
    if s:
        __watchlists_modify_body()
    else:
        ui.label('You are not logged in.').style('color: red')
        ui.button("Return Home", on_click=lambda: ui.navigate.to('/'))

    uit_footnote()



def __watchlists_modify_body():
    #common variables to use
    user_id = app.storage.user.get('user_id', None)
    selected_wl = None
    selected_op = None
    selected_itm = None


    #cards (what get shown)
    with ui.card() as part_intro:
        ui.label("What watchlist would you want to modify?")

        c = [{'name': 'list_name', 'field': 'list_name', 'label': "list_name"},
             {'name': 'list_id', 'field': 'list_id', 'label': "list_id"},
             {'name': 'creation_date', 'field': 'creation_date', 'label': 'creation_date'}]
        cur.execute("SELECT list_id, list_name, creation_date FROM watchlists WHERE user_id=%s", [user_id])
        r = cur.fetchall()
        part_i_table = ui.table(columns=c, rows=r, selection='single', row_key='list_id', on_select=lambda e:__select_watchlist(e))

        ui.label("What operation would you want to do?")
        with ui.row():
            ui.button("Add New Item", on_click=lambda: __select_operation('a'))
            ui.button("Remove Item", on_click=lambda: __select_operation('r'))
        with ui.row().classes('w-full justify-end'):
            ui.button("Next", on_click=lambda: __leave_step_intro())

    with ui.card() as part_add:
        ui.label("Add new watchlist")
        c = [{'name': 'title', 'field': 'title', 'label': "title"},
             {'name': 'release_date', 'field': 'release_date', 'label': "release_date"},
             {'name': 'runtime', 'field': 'runtime', 'label': "runtime"},
             {'name': 'genres', 'field': 'genres', 'label': "genres"},
             {'name': 'adult', 'field': 'adult', 'label': "adult"},
             {'name': 'budget', 'field': 'budget', 'label': "budget"},
             {'name': 'revenue', 'field': 'revenue', 'label': "revenue"},
             {'name': 'movie_id', 'field': 'movie_id', 'label': "movie_id"}]
        part_a_table = ui.table(columns=c, rows=[], selection='single', row_key='movie_id', on_select=lambda e:__select_item(e), pagination=100).style('width: 73vw')
        ui.input("Search Table...").bind_value(part_a_table, 'filter')
        ui.button('Add to List', on_click=lambda: __leave_step_add())

    with ui.card() as part_remove:
        ui.label("Remove watchlist")
        c = [{'name': 'title', 'field': 'title', 'label': "title"},
             {'name': 'release_date', 'field': 'release_date', 'label': "release_date"},
             {'name': 'runtime', 'field': 'runtime', 'label': "runtime"},
             {'name': 'genres', 'field': 'genres', 'label': "genres"},
             {'name': 'adult', 'field': 'adult', 'label': "adult"},
             {'name': 'budget', 'field': 'budget', 'label': "budget"},
             {'name': 'revenue', 'field': 'revenue', 'label': "revenue"},
             {'name': 'movie_id', 'field': 'movie_id', 'label': "movie_id"},
             {'name': 'add_date', 'field': 'add_date', 'label': "add_date"}]
        part_r_table = ui.table(columns=c, rows=[], selection='single', row_key='movie_id', on_select=lambda e:__select_item(e))
        ui.button('Remove', on_click=lambda: __leave_step_remove())

    with ui.card() as part_end:
        ui.label("Watchlist Modified")
        ui.button("Go Back to Watchlists", on_click=lambda: ui.navigate.to("/watchlists"))



    #SELECTIONS, FOR STORING INFORMATION FOR USE
    def __select_watchlist(e):
        if len(e.selection) != 0:   #error check
            nonlocal selected_wl    #global vars don't work here
            selected_wl = e.selection[0]['list_id']
            #print(selected_wl)
    def __select_operation(i):
        nonlocal selected_op
        selected_op = i     #'a' = add, 'r' = remove
    def __select_item(e):
        if len(e.selection) != 0:   #error check
            nonlocal selected_itm
            selected_itm = e.selection[0]['movie_id']
            #print(selected_itm)

    #PROCESSES, FOR GOING BETWEEN STEPS
    def __leave_step_intro():
        #print("globals, ", selected_wl, selected_op)
        if selected_op is None or selected_wl is None:
            ui.notify("Fill out all entries", color='negative')
            return #go back

        #else, enter the next step, based on what was chosen
        part_intro.set_visibility(False)

        if selected_op == 'a':      #add
            cur.execute("SELECT * FROM movies" +
                        " WHERE movie_id NOT IN (SELECT movie_id FROM watchlist_items WHERE list_id=%s)" +
                        " ORDER BY title ASC", [selected_wl])
            part_a_table.add_rows(cur.fetchall())
            part_a_table.update()
            part_add.set_visibility(True)
            return
        elif selected_op == 'r':    #remove
            cur.execute("SELECT * FROM watchlist_items as a JOIN movies as b ON a.movie_id=b.movie_id WHERE list_id=%s ORDER BY add_date DESC", [selected_wl])
            part_r_table.add_rows(cur.fetchall())
            part_r_table.update()
            part_remove.set_visibility(True)
            return

    def __leave_step_add():
        cur.execute("INSERT INTO watchlist_items (list_id, movie_id, add_date) VALUES (%s, %s, (SELECT CURRENT_TIMESTAMP))", [selected_wl, selected_itm])
        conn.commit()
        ui.notify("Added item to watchlist", color='positive')
        part_add.set_visibility(False)
        part_end.set_visibility(True)



    def __leave_step_remove():
        cur.execute("DELETE FROM watchlist_items WHERE list_id=%s AND movie_id=%s", [selected_wl, selected_itm])
        conn.commit()
        ui.notify("Deleted item from watchlist", color='positive')
        part_remove.set_visibility(False)
        part_end.set_visibility(True)



    part_intro.set_visibility(True)
    part_add.set_visibility(False)
    part_remove.set_visibility(False)
    part_end.set_visibility(False)



@ui.page('/watchlists_delete')
def __watchlists_delete():
    uit_banner()

    # Deny access to not logged-in users
    s = check_login()
    if s:
        __watchlists_delete_body()
    else:
        ui.label('You are not logged in.').style('color: red')
        ui.button("Return Home", on_click=lambda: ui.navigate.to('/'))

    uit_footnote()

@ui.refreshable
def __watchlists_delete_body():
    user_id = app.storage.user.get('user_id', None)
    wl_ids_names = __get_watchlist_ids_names(user_id)  #get dictionary of key-value pairs (id to name)

    ui.label("Enter list to delete:")
    selected_wl = ui.select(wl_ids_names)

    with ui.dialog() as d, ui.card():
        ui.label("Are you sure you want to delete this watchlist?")
        with ui.row().classes('w-full justify-between'):
            ui.button('🗑️Yes', on_click=lambda: __try_wl_delete(selected_wl.value, user_id)).props('color=red').style('width: 7vw')
            ui.space()
            ui.button('No', on_click=d.close).style('width: 7vw')

    ui.button('Delete List', on_click=d.open).props('color: red')

def __try_wl_delete(s_wl, user_id):
    #stop if user hadn't put in anything yet
    if s_wl is None :
        ui.notify('Enter a list to delete', color='negative')
        return

    cur.execute("DELETE FROM watchlists WHERE list_id=%s AND user_id=%s", [s_wl, user_id])
    conn.commit()

    __watchlists_delete_body.refresh()
    ui.notify('Watchlist deleted', color='positive')



''' 
Misc Functionality
'''
# find all watchlists you have made, and format them into a dictionary
# (good for ui.select, because then u get to tie both the name and id together)
def __get_watchlist_ids_names(user_id):
    cur.execute("SELECT list_id, list_name FROM watchlists WHERE user_id=%s ORDER BY creation_date", [user_id])
    list_ids_names = cur.fetchall()

    wl_output = {}

    for l_dn in list_ids_names:
        l_i = l_dn['list_id']
        l_n = l_dn['list_name']

        #add new key-value pair
        wl_output[l_i] = l_n

    return wl_output