import csv
import psycopg2
import psycopg2.extras
from tqdm import tqdm


#Log into the PgAdmin SQL Server
from db_info_test import *  #Info for logging into PgAdmin SQL server

conn = psycopg2.connect(
    host="dbclass.rhodescs.org",
    database="practice",
    user=DBUSER,
    password=DBPASS
)
cur = conn.cursor()



'''
Needed Functions
'''
#Converts file name + extension into file path.
def di_getpath(csv_file):
    csv_path = "./csv_files/" + csv_file
    print(f"reading: {csv_path}")
    return csv_path

#count total number of rows
#   parameter: the file path
#   returns: row count
def di_count_rows(csv_path):
    with open(csv_path, encoding="utf8") as f:
        total_rows = sum(1 for _ in f) - 1

    print(f"Total rows: {total_rows}")
    return total_rows


#Data validation when inserting data
#   (a.k.a., check if data is blank)
def clean(value):
    if value is None or value == "":
        return None
    return value    # PostgreSQL will parse YYYY-MM-DD

#for closing the importer
def di_closing():
    cur.close()
    conn.close()
    print("Import complete!")
