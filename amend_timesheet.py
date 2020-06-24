# todo The admin chooses a particular day and
#  edits the clockon/clockoff time for a particular employee for a particular day.

# todo get the employee selected
# todo get the date selected
# todo display the clock on / clock off dates for the employee+date
# todo update the clock on / clock off dates

from clockOn import employee_list, get_emp_list
import sqlite3
import tkcalendar
import tkinter.ttk
from datetime import datetime

db = sqlite3.connect('Timesheet.db')
acursor = db.cursor()
get_emp_list()


class AlterHours:

    def __init__(self):
        self.selected_employee = None
        self.selected_date = datetime.strftime(datetime.utcnow(), '%d-%b-%Y')


    def get_emp_id(self, employee_name):
        sql_get_id = "SELECT emp_id FROM employee WHERE name=?"
        emp_id = acursor.execute(sql_get_id, (employee_name,)).fetchone()
        print(emp_id)
        return emp_id

    # EMPLOYEE SELECT
    def employee_select(self, event):
        self.selected_employee = event.widget.get()  # todo select user here
        print(self.selected_employee)
        self.update_time()

    # DATE SELECT
    def date_select(self, event):
        selected_date = event.widget.get_date()
        self.selected_date = datetime.strftime(selected_date, '%d-%b-%Y')
        print(self.selected_date)
        self.update_time()

    def show_clock(self, on=True):
        # SHOW CLOCK ON / CLOCK OFF TIMES GIVEN DATE AND EMPLOYEE
        sql_clockon = "SELECT clock_on FROM timestamp WHERE (emp_id=? AND date=?)"
        sql_clockoff = "SELECT clock_off FROM timestamp WHERE (emp_id=? AND date=?)"
        emp_id = self.get_emp_id(self.selected_employee)[0]
        clock_on = acursor.execute(sql_clockon, (emp_id, self.selected_date)).fetchone()
        clock_off = acursor.execute(sql_clockoff, (emp_id, self.selected_date)).fetchone()
        print(clock_on)
        print(clock_off)
        print('bab')
        if clock_on:
            if clock_off[0]:
                return clock_on, clock_off
            else:
                return clock_on, 'None'
        else:
            return 'None', 'None'

    def alter_clock(self):
            # ALTER THE CLOCK ON/ CLOCK OFF DATES
            alter_clock_on = '13:00'  # todo alter time here
            alter_clock_off = '17:00'  # todo alter time here

            # logic to decide time to update.
            change_clock_on = False
            if change_clock_on:
                sql_change_time = "UPDATE timestamp SET {0} = ? WHERE (emp_id=? AND date=?)".format('clock_on')
                acursor.execute(sql_change_time, (alter_clock_on, self.get_emp_id(self.selected_employee), self.selected_date))
            else:
                sql_change_time = "UPDATE timestamp SET {0} = ? WHERE (emp_id=? AND date=?)".format('clock_off')
                acursor.execute(sql_change_time, (alter_clock_off, self.get_emp_id(self.selected_employee), self.selected_date))

            db.commit()

    def update_time(self):
        clock_on_time['text'] = self.show_clock(True)[0]
        clock_off_time['text'] = self.show_clock(False)[1]


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
root.rowconfigure(5, weight=3)

# Initialize AlterHour
alter = AlterHours()

# USER SELECTBOX
emp_options = tkinter.ttk.Combobox(root, values=employee_list, state='readonly')
emp_options.grid(row=1, column=1, columnspan=2, sticky='nw')
emp_options.bind('<<ComboboxSelected>>', alter.employee_select)

# DATE SELECT
datepicker = tkinter.Entry(root)
datepicker.grid(row=2, column=1, sticky='nw')
calender = tkcalendar.DateEntry(datepicker, locale='en_AU', date_pattern='dd-m-yy')
calender.grid(row=0, column=1)
calender.bind('<<DateEntrySelected>>', alter.date_select)

# CLOCK ON / OFF LABEL
clock_on_label = tkinter.Label(root, text='Clock On: ')
clock_on_label.grid(row=3, column=1, sticky='nw')

clock_off_label = tkinter.Label(root, text='Clock Off: ')
clock_off_label.grid(row=4, column=1, sticky='nw')

# CLOCK ON / OFF TIME DISPLAY

# todo up to here, need to make the time display given the user id and date.
clock_on_time = tkinter.Label(root, text='None')
clock_on_time.grid(row=3, column=2, sticky='nw')

clock_off_time = tkinter.Label(root, text='None')
clock_off_time.grid(row=4, column=2, sticky='nw')




root.mainloop()
