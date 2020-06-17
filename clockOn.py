import tkinter
import tkinter.ttk
import datetime
import sqlite3

db = sqlite3.connect('Timesheet.db')
acursor = db.cursor()

# Main window instantiated
rootWindow = tkinter.Tk()

# Title and initial opening frame size.
rootWindow.title('ClockOn')
rootWindow.geometry('300x300')

# Configure row/column layout
rootWindow.columnconfigure(0, weight=1)
rootWindow.columnconfigure(1, weight=1)
rootWindow.columnconfigure(2, weight=1)
rootWindow.columnconfigure(3, weight=1)
rootWindow.rowconfigure(0, weight=1)
rootWindow.rowconfigure(1, weight=1)
rootWindow.rowconfigure(2, weight=1)
rootWindow.rowconfigure(3, weight=1)
rootWindow.rowconfigure(4, weight=1)


def get_current_time():
    cur_time = datetime.datetime.now().strftime('%H:%M')
    return cur_time


def get_current_date():
    cur_date = datetime.datetime.now().strftime('%d-%b-%Y')
    return cur_date


class Timestamp:

    def __init__(self, clock_in=None, clock_out=None, name=None, date=None):
        self.clock_in = clock_in
        self.clock_out = clock_out
        self.name = name
        self.date = date

        self.clock_on_status = None
        self.clock_off_status = None

    # These status' check for clockin/clockout to see if it is empty.
    def status_update(self):
        emp_id = self.get_emp_id()
        self.clock_on_status = acursor.execute('SELECT clock_on FROM timestamp WHERE emp_id=?', (emp_id,)).fetchone()
        self.clock_off_status = acursor.execute('SELECT clock_off FROM timestamp WHERE emp_id=?', (emp_id,)).fetchone()
        self.user_status(self.clock_on_status, self.clock_off_status)

    def emp_select(self, event):
        self.name = event.widget.get()
        self.status_update()

    def emp_clock_in(self):
        print('clocked on')
        # inserts clock on time/ emp_id and date into the timestamp table.
        acursor.execute('INSERT INTO timestamp (clock_on, emp_id, date) VALUES (?,?,?)',
                        (get_current_time(), self.get_emp_id(), get_current_date()))
        db.commit()
        self.status_update()

    def emp_clock_out(self):
        print('clocked out')
        acursor.execute('UPDATE timestamp SET clock_off = ? WHERE emp_id = ?', (get_current_time(), self.get_emp_id()))
        db.commit()
        self.status_update()

    def get_emp_id(self):
        sql_get_id = "SELECT emp_id FROM employee WHERE name=?"
        emp_id = acursor.execute(sql_get_id, (self.name,)).fetchone()[0]
        return emp_id

    def user_status(self, clock_on_stat, clock_off_stat):
        # when the clock in button is clicked. The button is disabled.
        if clock_on_stat is None:
            clock_on['state'] = 'enabled'
            clock_off['state'] = 'disabled'
        if clock_on_stat:
            print('this is run')
            if clock_off_stat[0]:
                clock_on['state'] = 'disabled'
                clock_off['state'] = 'disabled'
            else:
                clock_on['state'] = 'disabled'
                clock_off['state'] = 'enabled'


def get_emp_list():
    for row in acursor.execute("SELECT name FROM employee").fetchall():
        employee_list.append(row[0])


emp_record = Timestamp()
employee_list = []
get_emp_list()

# Construct the Option menu and populate it with employees
emp_options = tkinter.ttk.Combobox(rootWindow, values=employee_list, state='readonly')
emp_options.grid(row=1, column=1, columnspan=2, sticky='new')
# Event(the box item being clicked) assigned to a handler(function get_employee).
emp_options.bind('<<ComboboxSelected>>', emp_record.emp_select)

# Clock on and off buttons
clock_on = tkinter.ttk.Button(rootWindow, text='Clock On', command=emp_record.emp_clock_in)
clock_on.grid(row=2, column=1, sticky='nw')

clock_off = tkinter.ttk.Button(rootWindow, text='Clock Off', command=emp_record.emp_clock_out)
clock_off.grid(row=3, column=1, sticky='nw')

rootWindow.mainloop()
