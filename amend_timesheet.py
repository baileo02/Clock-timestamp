# todo The admin chooses a particular day and
#  edits the clockon/clockoff time for a particular employee for a particular day.

# todo get the employee selected
# todo get the date selected
# todo display the clock on / clock off dates for the employee+date
# todo update the clock on / clock off dates

from clockOn import employee_list, get_emp_list, emp_options

import sqlite3
import tkinter

db = sqlite3.connect('Timesheet.db')
acursor = db.cursor()

# EMPLOYEE SELECT
get_emp_list()
print(employee_list)

selected_employee = employee_list[0]  # todo select user here
print(selected_employee)


def get_emp_id(employee_name):
    sql_get_id = "SELECT emp_id FROM employee WHERE name=?"
    emp_id = acursor.execute(sql_get_id, (employee_name,)).fetchone()[0]
    return emp_id


print(get_emp_id(selected_employee))

# DATE SELECT
selected_date = '11-Jun-2020'  # todo select date here

# SHOW CLOCK ON / CLOCK OFF TIMES GIVEN DATE AND EMPLOYEE
sql_clockon = "SELECT clock_on FROM timestamp WHERE (emp_id=? AND date=?)"
sql_clockoff = "SELECT clock_off FROM timestamp WHERE (emp_id=? AND date=?)"

clock_on = acursor.execute(sql_clockon, (get_emp_id(selected_employee), selected_date)).fetchone()[0]
clock_off = acursor.execute(sql_clockoff, (get_emp_id(selected_employee), selected_date)).fetchone()[0]

print(clock_on, clock_off)

# ALTER THE CLOCK ON/ CLOCK OFF DATES
alter_clock_on = '13:00'  # todo alter time here
alter_clock_off = '17:00'  # todo alter time here

# logic to decide time to update.
change_clock_on = False
if change_clock_on:
    sql_change_time = "UPDATE timestamp SET {0} = ? WHERE (emp_id=? AND date=?)".format('clock_on')
    acursor.execute(sql_change_time, (alter_clock_on, get_emp_id(selected_employee), selected_date))
else:
    sql_change_time = "UPDATE timestamp SET {0} = ? WHERE (emp_id=? AND date=?)".format('clock_off')
    acursor.execute(sql_change_time, (alter_clock_off, get_emp_id(selected_employee), selected_date))

db.commit()

# CONFIGURE DISPLAY
root = tkinter.Tk()
root.geometry('300x300')

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=1)

# USER SELECTBOX





root.mainloop()
