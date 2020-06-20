import tkinter
import sqlite3
import clockOn
from clockOn import get_emp_list, employee_list
from datetime import datetime
from datetime import timedelta

db = sqlite3.connect('Timesheet.db')
acursor = db.cursor()

display_week = []
date_list = []
hours_list = []

# Functions are from clockOn module. Gets all employees and appends it to employee_list
get_emp_list()


# Deals with creating columns and rows and populating it with data
class DisplayGrid(object):

    def __init__(self, window):
        self.window = window

    # Base function that iterates and populates a row or column given a list.
    def cell_create(self, data_list, start_index, is_column=True, row=0,
                    column=0):  # is_column specifies to populate row or column
        for counter, header in enumerate(data_list, start_index):
            label = tkinter.Label(self.window, text=header)

            # True by default, this will place the entry horizontally
            if is_column:
                label.grid(row=row, column=counter, sticky='new')
                label.config(borderwidth=1, relief='solid')
            # Will place the entry vertically.
            else:
                label.grid(row=counter, column=column, sticky='new')
                label.config(borderwidth=1, relief='solid')
                self.window.rowconfigure(counter, weight=3)


# Grab weeks worth of dates given the initial date, and stores it in date_list as string ready to use by database.
def generate_dates():
    # Holds the dates as date type to allow timedelta calculations
    date_object_list = []
    # todo needs to be gotten from user input
    # todo make a datepicker of some sort
    initial_date = '15-Jun-2020'
    # Append date_object of initial date to date_object list
    date_object = datetime.strptime(initial_date, '%d-%b-%Y')
    date_object_list.append(date_object)
    # Iterates through 7 times and appends the dates as date type
    for i in range(1, 7):
        date_object += timedelta(days=1)
        date_object_list.append(date_object)
    # Grabs the date object list and converts back to string and appends it to the date_list.
    for date in date_object_list:
        # date_list for hour calculation
        date_list.append(datetime.strftime(date, '%d-%b-%Y'))
        # display_week for header display
        display_week.append(datetime.strftime(date, '%d-%b'))
    display_week.append('Total')
    print(display_week)


# Calculates and returns two times in the format '24H:60M' and returns the (minutes, hours) in a tuple
def calc_hours(clockon, clockoff):
    if clockoff:
        c_off_hour = datetime.strptime(clockoff, '%H:%M')
        c_on_hour = datetime.strptime(clockon, '%H:%M')

        seconds_diff = (c_off_hour - c_on_hour).seconds
        minutes = (seconds_diff // 60) % 60
        hours = seconds_diff // 3600

        return int(hours), int(minutes)
    else:
        return None


# calculates total hour given a list tuple and returns it as a tuple (total hour, total minutes)
def calc_total(timelist):
    f_timelist = [x for x in timelist if x is not None]
    total_hour = sum(hr for hr, m in f_timelist)
    overflow_min = sum(m for hr, m in f_timelist)
    total_hour += overflow_min // 60
    total_min = overflow_min % 60

    return str(total_hour) + 'hr', str(total_min) + 'min'


# Grabs each employees hours + total hours and stores it in hours_list and displays it.
def get_hours():
    for counter, employee in enumerate(employee_list, 1):
        sql_get_id = "SELECT emp_id FROM employee WHERE name=?"
        emp_id = acursor.execute(sql_get_id, (employee,)).fetchone()[0]
        temp_hour = []
        for date in date_list:
            sql_clockon = "SELECT clock_on FROM timestamp WHERE (emp_id=? AND date=?)"
            sql_clockoff = "SELECT clock_off FROM timestamp WHERE (emp_id=? AND date=?)"
            sql_date = "SELECT date FROM timestamp WHERE (emp_id=? AND date=?)"
            check_date = acursor.execute(sql_date, (emp_id, date)).fetchone()
            check_clock_off = acursor.execute(sql_clockoff, (emp_id, date)).fetchone()
            # check date assumes clock on is filled in as clocking on fills in both date and clock in time together
            if check_date:
                if check_clock_off:
                    hours = calc_hours(acursor.execute(sql_clockon, (emp_id, date)).fetchone()[0],
                                       acursor.execute(sql_clockoff, (emp_id, date)).fetchone()[0])
                    temp_hour.append(hours)
            else:
                # Appends None if date doesnt exist (i.e. employee did not work that day)
                # OR if employee forgets to clock off
                temp_hour.append(None)
        temp_hour.append(calc_total(temp_hour))
        display.cell_create(temp_hour, 1, True, row=counter)


# Main window initialization
rootWindow = tkinter.Tk()
rootWindow.title('Display Hours')
rootWindow.geometry('600x600')
# Main window column/row configure
rootWindow.columnconfigure(0, weight=1)
rootWindow.rowconfigure(0, weight=1)
rootWindow.rowconfigure(1, weight=5)

# Top frame which will contain the date selector
top_frame = tkinter.Frame(rootWindow)
top_frame.grid(row=0, column=0, sticky='nsew')
top_frame.config(borderwidth=1, relief='solid')
# Configure column/row for top_frame
top_frame.columnconfigure(0, weight=1)
top_frame.columnconfigure(1, weight=3)
top_frame.columnconfigure(2, weight=1)
top_frame.rowconfigure(0, weight=1)

# Display frame will contain the weekday/total and hours + employee
display_frame = tkinter.Frame(rootWindow)
display_frame.grid(row=1, column=0, sticky='nsew')
# display_frame.config(borderwidth=1, relief='solid')
# Configure column/row for display_frame
display_frame.columnconfigure(0, weight=2)
display_frame.columnconfigure(1, weight=2)
display_frame.columnconfigure(2, weight=2)
display_frame.columnconfigure(3, weight=2)
display_frame.columnconfigure(4, weight=2)
display_frame.columnconfigure(5, weight=2)
display_frame.columnconfigure(6, weight=2)
display_frame.columnconfigure(7, weight=2)
display_frame.columnconfigure(8, weight=2)
display_frame.rowconfigure(0, weight=1)
# display_frame.rowconfigure(1, weight=1)

# Initialize DisplayGrid
display = DisplayGrid(display_frame)

generate_dates()
get_hours()

# Create Week/total column
display.cell_create(display_week, 1)
# Create employee list rows
display.cell_create(employee_list, 1, is_column=False)

top_label = tkinter.Label(top_frame, text='hello')
top_label.grid(row=0, column=1, sticky='w')

rootWindow.mainloop()
