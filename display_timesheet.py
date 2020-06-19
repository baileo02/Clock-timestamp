import tkinter
import sqlite3
import clockOn
from clockOn import get_emp_list, employee_list
from datetime import datetime
from datetime import timedelta

display_week = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun', 'Total']
date_list = []
# Functions are from clockOn module. Gets all employees and appends it to employee_list
get_emp_list()


# Deals with creating columns and rows and populating it with data
class DisplayGrid(object):

    def __init__(self, window):
        self.window = window

    # Base function that iterates and populates a row or column given a list.
    def cell_create(self, data_list, start_index, is_column=True):  # is_column specifies to populate row or column
        for counter, header in enumerate(data_list, start_index):
            label = tkinter.Label(self.window, text=header)

            if is_column:
                label.grid(row=0, column=counter, sticky='new')
                label.config(borderwidth=1, relief='solid')
            else:
                label.grid(row=counter, column=0, sticky='new')
                label.config(borderwidth=1, relief='solid')
                self.window.rowconfigure(counter, weight=3)


# Grab weeks worth of dates given the initial date, and stores it in date_list as string ready to use by database.
def generate_dates():
    # Holds the dates as date type to allow timedelta calculations
    date_object_list = []
    initial_date = '08-Jun-2020'    # todo needs to be gotten from user input later.
    # Append date_object of initial date to date_object list
    date_object = datetime.strptime(initial_date, '%d-%b-%Y')
    date_object_list.append(date_object)
    # Iterates through 7 times and appends the dates as date type
    for i in range(1, 8):
        date_object += timedelta(days=1)
        date_object_list.append(date_object)
    # Grabs the date object list and converts back to string and appends it to the date_list.
    for date in date_object_list:
        date_list.append(datetime.strftime(date, '%d-%b-%Y'))



# todo for each iterated date, get the clock on/off time for the specified employee (name -> emp_id)
# todo get the time difference and output it into a list
# todo feed the list into the display.cell_create method.







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
# Create Week/total column
display.cell_create(display_week, 1)
# Create employee list rows
display.cell_create(employee_list, 1, is_column=False)












top_label = tkinter.Label(top_frame, text='hello')
top_label.grid(row=0, column=1, sticky='w')




# todo configured the widget, need to add the weekdays and logic shit for the stuff
# todo tomorrow. in the class, initialize the titles, (mon-sun + total)
# todo then given a date. get the clock in/out times of that date +1+1+1 for the week
# todo put them in a list and place them across the columns.


rootWindow.mainloop()
