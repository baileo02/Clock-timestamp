import tkinter
import sqlite3
from datetime import datetime
from datetime import timedelta
import tkcalendar
from database_connection import Database



# Deals with creating columns and rows and populating it with data
class DisplayGrid:

    def __init__(self, window, db):
        self.window = window
        self.hour_list = []
        self.date_list = []
        self.weekHeader = []
        self.hour_list_display = []
        self.db = db

        self.initial_date = datetime.strftime(datetime.now(), '%Y-%m-%d')
        # get_emp_list is from clockOn module. Gets all employees and appends it to employee_list
        self.employee_list = []
        self.get_emp_list()

        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=5)

        self.top_frame = tkinter.Frame(self.window)
        self.top_frame.grid(row=0, column=0, sticky='nsew')
        self.top_frame.config(borderwidth=1, relief='solid')
        # Configure column/row for top_frame
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.columnconfigure(1, weight=3)
        self.top_frame.columnconfigure(2, weight=1)
        self.top_frame.rowconfigure(0, weight=1)

        self.display_frame = tkinter.Frame(self.window)
        self.display_frame.grid(row=1, column=0, sticky='nsew')
        # Configure column/row for display_frame
        self.display_frame.columnconfigure(0, weight=2)
        self.display_frame.columnconfigure(1, weight=2)
        self.display_frame.columnconfigure(2, weight=2)
        self.display_frame.columnconfigure(3, weight=2)
        self.display_frame.columnconfigure(4, weight=2)
        self.display_frame.columnconfigure(5, weight=2)
        self.display_frame.columnconfigure(6, weight=2)
        self.display_frame.columnconfigure(7, weight=2)
        self.display_frame.columnconfigure(8, weight=2)
        self.display_frame.rowconfigure(0, weight=1)

        self.datepicker = tkinter.Entry(self.top_frame)
        self.datepicker.grid(row=0, column=1, sticky='w')
        self.calender = tkcalendar.DateEntry(self.datepicker, locale='en_AU', date_pattern='y-mm-dd')
        self.calender.grid(row=0, column=1)
        self.calender.bind('<<DateEntrySelected>>', self.date_select)
        self.generate_headers(self.display_frame)
        self.generate_hours(self.display_frame)

    def get_emp_list(self):
        for row in self.db.acursor.execute("SELECT name FROM employee").fetchall():
            self.employee_list.append(row[0]) if row[0] not in self.employee_list else self.employee_list


# Base function that iterates and populates a row or column given a list.
    def cell_create(self, window, data_list, row, column, is_column, start_index):  # is_column specifies to populate row or column
        for counter, header in enumerate(data_list, start_index):
            label = tkinter.Label(window, text=header)

            # True by default, this will place the entry horizontally
            if is_column:
                label.grid(row=row, column=counter, sticky='new')
                label.config(borderwidth=1, relief='solid')
            # Will place the entry vertically.
            else:
                label.grid(row=counter, column=column, sticky='new')
                label.config(borderwidth=1, relief='solid')
                window.rowconfigure(counter, weight=3)

    # Generates week/employee headers and feeds it to cell_create to display the data.
    def generate_headers(self, bottom_window):
        self.generate_dates()
        self.cell_create(bottom_window, self.weekHeader, 0, 0, True, 1)
        self.cell_create(bottom_window, self.employee_list, 0, 0, False, 1)

    # Loops through the list of employees and their hours for a specific week and compiles it in hours_list
    # hours_list is fed to cell_Create to display
    def generate_hours(self, bottom_window):
        for counter, employee in enumerate(self.employee_list, 1):
            emp_id = self.get_emp_id(employee)
            for date in self.date_list:
                self.day_hour(emp_id, date)
            # this appends the total to the hour_list
            self.hour_list_display.append(calc_total(self.hour_list))
            self.cell_create(bottom_window, self.hour_list_display, counter, 1, True, 1)
            self.hour_list_display.clear()
            self.hour_list.clear()

    def reselect_date(self):
        self.clearlist()
        self.generate_headers(self.display_frame)
        self.generate_hours(self.display_frame)

    def clearlist(self):
        self.hour_list.clear()
        self.weekHeader.clear()
        self.date_list.clear()
        self.hour_list_display.clear()

    # Grab weeks worth of dates given the initial date, and stores it in date_list as string ready to use by database.
    def generate_dates(self):
        # Holds the dates as date type to allow timedelta calculations
        date_object_list = []
        # Append date_object of initial date to date_object list
        date_object = datetime.strptime(self.initial_date, '%Y-%m-%d')
        date_object_list.append(date_object)
        # Iterates through 7 times and appends the dates as date type
        for i in range(1, 7):
            date_object += timedelta(days=1)
            date_object_list.append(date_object)
        # Grabs the date object list and converts back to string and appends it to the date_list.
        for date in date_object_list:
            # date_list for hour calculation
            self.date_list.append(datetime.strftime(date, '%Y-%m-%d'))
            # weekHeader for header display
            self.weekHeader.append(datetime.strftime(date, '%d-%b'))
        self.weekHeader.append('Total')


    def day_hour(self, emp_id, date):
        sql_clockon = "SELECT clock_on FROM timestamp WHERE (emp_id=? AND date=?)"
        sql_clockoff = "SELECT clock_off FROM timestamp WHERE (emp_id=? AND date=?)"
        sql_date = "SELECT date FROM timestamp WHERE (emp_id=? AND date=?)"
        check_date = self.db.acursor.execute(sql_date, (emp_id, date)).fetchone()
        check_clock_off = self.db.acursor.execute(sql_clockoff, (emp_id, date)).fetchone()
        check_clock_on = self.db.acursor.execute(sql_clockon, (emp_id, date)).fetchone()
        # check date assumes clock on is filled in as clocking on fills in both date and clock in time together
        if check_date:
            if check_clock_off[0]:
                hours = calc_hours(self.db.acursor.execute(sql_clockon, (emp_id, date)).fetchone()[0],
                                   self.db.acursor.execute(sql_clockoff, (emp_id, date)).fetchone()[0])
                self.hour_list_display.append(hours)
                self.hour_list.append(hours)

            else:
                self.hour_list_display.append('AMEND')
        else:

            # date doesnt exist
            self.hour_list_display.append(None)
            self.hour_list.append(None)

    def date_select(self, event):
        selected_date = event.widget.get_date()
        self.initial_date = datetime.strftime(selected_date, '%Y-%m-%d')
        self.reselect_date()



    def get_emp_id(self, employee_name):
        sql_get_id = "SELECT emp_id FROM employee WHERE name=?"
        emp_id = self.db.acursor.execute(sql_get_id, (employee_name,)).fetchone()[0]
        return emp_id


# Calculates and returns two times in the format '24H:60M' and returns the (minutes, hours) in a tuple
# todo for records with clock off time but NO CLOCK ON TIMES wont show up.
# todo problem can be recreated when you use amend_timesheet and insert and clock off time.
def calc_hours(clockon, clockoff):
    if clockoff and clockon:
        c_off_hour = datetime.strptime(clockoff, '%H:%M')
        c_on_hour = datetime.strptime(clockon, '%H:%M')

        seconds_diff = ((c_off_hour - c_on_hour) - timedelta(seconds=1800)).seconds
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


if __name__ == '__main__':

    # Initialize DisplayGrid
    database = Database('timesheet2.db')
    acursor = database.acursor
    # Main window initialization
    rootWindow = tkinter.Tk()
    dp = DisplayGrid(rootWindow, database)
    rootWindow.title('Display Hours')
    rootWindow.geometry('600x600')
    # Main window column/row configure
    rootWindow.columnconfigure(0, weight=1)
    rootWindow.rowconfigure(0, weight=1)
    rootWindow.rowconfigure(1, weight=5)

    # Top frame which will contain the date selector
    # top_frame = tkinter.Frame(rootWindow)
    # top_frame.grid(row=0, column=0, sticky='nsew')
    # top_frame.config(borderwidth=1, relief='solid')
    # # Configure column/row for top_frame
    # top_frame.columnconfigure(0, weight=1)
    # top_frame.columnconfigure(1, weight=3)
    # top_frame.columnconfigure(2, weight=1)
    # top_frame.rowconfigure(0, weight=1)

    # Display frame will contain the weekday/total and hours + employee
    # display_frame = tkinter.Frame(rootWindow)
    # display_frame.grid(row=1, column=0, sticky='nsew')
    # # Configure column/row for display_frame
    # display_frame.columnconfigure(0, weight=2)
    # display_frame.columnconfigure(1, weight=2)
    # display_frame.columnconfigure(2, weight=2)
    # display_frame.columnconfigure(3, weight=2)
    # display_frame.columnconfigure(4, weight=2)
    # display_frame.columnconfigure(5, weight=2)
    # display_frame.columnconfigure(6, weight=2)
    # display_frame.columnconfigure(7, weight=2)
    # display_frame.columnconfigure(8, weight=2)
    # display_frame.rowconfigure(0, weight=1)

    # datepicker = tkinter.Entry(top_frame)
    # datepicker.grid(row=0, column=1, sticky='w')
    # calender = tkcalendar.DateEntry(datepicker, locale='en_AU', date_pattern='dd-m-yy')
    # calender.grid(row=0, column=1)
    # calender.bind('<<DateEntrySelected>>', dp.date_select)
    # dp.generate_headers(display_frame)
    # dp.generate_hours(display_frame)

    #todo need to make display_timesheet portable for main.py







    rootWindow.mainloop()
