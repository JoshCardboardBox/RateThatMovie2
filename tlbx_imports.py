""""
Toolbox of Common Imports

    The file where we put our common imports.
"""

#Misc...
import random


### PsycoPG Setup...
import psycopg
from psycopg.rows import dict_row

# Connect to an existing database
from db_info import *
conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}")

# Open a cursor to perform database operations
cur = conn.cursor(row_factory=dict_row)



### NiceGui Setup...
import nicegui
from nicegui import ui, app
