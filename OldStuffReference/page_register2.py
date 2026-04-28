# Script to let us register students.

import psycopg
from psycopg.rows import dict_row
from OldStuffReference.dbinfo import *
from nicegui import ui, app

# Connect to an existing database
conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}")

# Open a cursor to perform database operations
cur = conn.cursor(row_factory=dict_row)

def get_students():
    cur.execute("SELECT student_id, first_name, last_name, grad_year FROM students")
    rows = cur.fetchall()
    return rows

def get_classes_for_student(student_id):
    cur.execute("SELECT * from enroll NATURAL JOIN courses WHERE student_id=%s", [student_id])
    rows = cur.fetchall()
    return rows

def get_non_conflicting_classes_for_student(student_id):
    cur.execute("SELECT * FROM courses WHERE start_time" +
                " NOT IN (SELECT start_time FROM enroll NATURAL JOIN courses WHERE student_id=%s)", [student_id])
    rows = cur.fetchall()
    return rows

@ui.page('/register2')
def register2():
    username = app.storage.user.get('username', None)
    if username is None:
        ui.navigate.to('/login?redirect_url=/register2')
        return

    selected_student = app.storage.user.get('username', None)
    selected_course = None
    def process_step1():
        schedule_rows = get_classes_for_student(selected_student)
        my_classes_table.add_rows(schedule_rows)
        my_classes_table.update()

        # Add code to add classes to avail_classes_table
        potential_classes = get_non_conflicting_classes_for_student(selected_student)
        avail_classes_table.add_rows(potential_classes)
        avail_classes_table.update()

        step2_card.set_visibility(True)

    with ui.card() as step2_card:
        ui.label("Student Schedule:")
        cols = [{'name': 'course_id', 'field': 'course_id', 'label': "Course ID"},
                {'name': 'department', 'field': 'department', 'label': "Dept"},
                {'name': 'course_number', 'field': 'course_number', 'label': "Course Num"},
                {'name': 'course_section', 'field': 'course_section', 'label': "Section"},
                {'name': 'start_time', 'field': 'start_time', 'label': "Time"}]
        my_classes_table = ui.table(columns=cols, rows=[])

        ui.label("Classes available:")
        avail_classes_table = ui.table(columns=cols, rows=[], selection='single', row_key='course_id',
                                       on_select=lambda e: click_course(e))

        process_step1()
        ui.button('Register!', on_click=lambda: process_step2())

    with ui.card() as step3_card:
        ui.label("New Schedule:")
        cols = [{'name': 'course_id', 'field': 'course_id', 'label': "Course ID"},
                {'name': 'department', 'field': 'department', 'label': "Department"},
                {'name': 'course_number', 'field': 'course_number', 'label': "Course Num"},
                {'name': 'course_section', 'field': 'course_section', 'label': "Section"},
                {'name': 'start_time', 'field': 'start_time', 'label': "Time"}]
        my_new_classes_table = ui.table(columns=cols, rows=[])

    step2_card.set_visibility(True)
    step3_card.set_visibility(False)

    def click_course(e):
        nonlocal selected_course
        print(e.selection)
        selected_course = e.selection[0]['course_id']


    def process_step2():
        # Add code to register the student for the class
        nonlocal selected_course

        print(selected_student)
        print(selected_course)
        cur.execute("INSERT INTO enroll (student_id, course_id) VALUES (%s,%s)", [selected_student, selected_course])
        conn.commit()

        # get the updated schedule
        schedule_rows = get_classes_for_student(selected_student)
        my_new_classes_table.add_rows(schedule_rows)
        my_new_classes_table.update()

        step2_card.set_visibility(False)
        step3_card.set_visibility(True)

# dont wanna tell nicegui to run twice
# run register login not resgier 2