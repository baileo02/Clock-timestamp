import tkinter
import tkinter.ttk
import datetime
from database_connection import Database


def get_current_time():
    cur_time = datetime.datetime.now().strftime('%H:%M')
    return cur_time


def get_current_date():
    cur_date = datetime.datetime.now().strftime('%Y-%m-%d')
    return cur_date


class Timestamp:

    def __init__(self, window, db, clock_in=None, clock_out=None, name=None, date=None):
        self.clock_in = clock_in
        self.clock_out = clock_out
        self.employee_list = []
        self.date = date
        self.window = window
        self.db = db

        # status of an employee for current day, if they have clocked on/off or at all.
        self.clock_on_status = None
        self.clock_off_status = None
        self.date_status = None

        self.get_emp_list()
        # Construct the Option menu and populate it with employees
        self.emp_options = tkinter.ttk.Combobox(self.window, values=self.employee_list, state='readonly')
        self.emp_options.grid(row=1, column=1, columnspan=2, sticky='new')
        # Event(the box item being clicked) assigned to a handler(function get_employee).
        self.emp_options.bind('<<ComboboxSelected>>', self.emp_select)

        # Clock on and off buttons
        self.clock_on = tkinter.ttk.Button(self.window, text='Clock On', command=self.emp_clock_in)
        self.clock_on.grid(row=2, column=1, sticky='nw')

        self.clock_off = tkinter.ttk.Button(self.window, text='Clock Off', command=self.emp_clock_out)
        self.clock_off.grid(row=3, column=1, sticky='nw')

        self.emp_options.current(0)
        self.name = self.emp_options.get()

        self.status_update()

        self.clock_on_label = tkinter.Label(self.window, text=self.clock_on_status)
        self.clock_on_label.grid(row=2, column=2, sticky='nw')
        # self.display_time()
        self.clock_off_label = tkinter.Label(self.window, text=self.clock_off_status)
        self.clock_off_label.grid(row=3, column=2, sticky='nw')


    # These status' check for clockin/clockout to see if it is empty.
    def status_update(self):
        emp_id = self.get_emp_id()
        self.clock_on_status = self.db.acursor.execute('SELECT clock_on FROM timestamp WHERE (emp_id=? AND date=?)',
                                                       (emp_id, get_current_date())).fetchone()
        self.clock_off_status = self.db.acursor.execute('SELECT clock_off FROM timestamp WHERE (emp_id=? AND date=?) ',
                                                        (emp_id,get_current_date())).fetchone()
        latest_date = self.db.acursor.execute('SELECT MAX(date) FROM timestamp WHERE emp_id=?', (emp_id,)).fetchone()[0]
        print(self.clock_on_status)
        print(get_current_date())
        print(latest_date)
        # todo might need to change the date time structure to YYYY-MM-DD HH:MM:SS.SSS. ISO standard.
        print(get_current_date() == latest_date)
        if get_current_date() == latest_date:

            self.date_status = True
        else:

            self.date_status = False

        self.user_status(self.clock_on_status, self.clock_off_status, self.date_status)

    def emp_select(self, event):
        self.name = event.widget.get()
        self.status_update()
        self.display_time()

    def emp_clock_in(self):
        print('clocked on')
        # inserts clock on time/ emp_id and date into the timestamp table.
        self.db.acursor.execute('INSERT INTO timestamp (clock_on, emp_id, date) VALUES (?,?,?)',
                                (get_current_time(), self.get_emp_id(), get_current_date()))
        self.display_time()
        self.db.db.commit()
        self.status_update()
        self.display_time()

    def emp_clock_out(self):
        print('clocked out')
        self.db.acursor.execute('UPDATE timestamp SET clock_off = ? WHERE (emp_id = ? AND date = ?)',
                                (get_current_time(), self.get_emp_id(), get_current_date()))
        self.display_time()
        self.db.db.commit()
        self.status_update()
        self.display_time()


    def get_emp_id(self):
        sql_get_id = "SELECT emp_id FROM employee WHERE name=?"
        emp_id = self.db.acursor.execute(sql_get_id, (self.name,)).fetchone()[0]
        return emp_id

    def user_status(self, clock_on_stat, clock_off_stat, date_stat):
        # todo clock off button can keep getting pressed needs to be more robust.
        if not date_stat:
            self.clock_on['state'] = 'enabled'
            self.clock_off['state'] = 'disabled'
        if clock_on_stat and date_stat:
            if clock_off_stat[0] and date_stat:
                self.clock_on['state'] = 'disabled'
                self.clock_off['state'] = 'enabled'
            else:
                self.clock_on['state'] = 'disabled'
                self.clock_off['state'] = 'enabled'

    # todo in future, if there is same names, this wont work, it should check by _id
    def get_emp_list(self):
        for row in self.db.acursor.execute("SELECT name FROM employee").fetchall():
            self.employee_list.append(row[0]) if row[0] not in self.employee_list else self.employee_list

    def display_time(self):
        if self.clock_on_status:
            self.clock_on_label.config(text=self.clock_on_status)
        else:
            self.clock_on_label.config(text='None')

        if self.clock_off_status:
            self.clock_off_label.config(text=self.clock_off_status)
        else:
            self.clock_off_label.config(text='None')




if __name__ == '__main__':
    # db = sqlite3.connect('Timesheet.db')
    # acursor = db.cursor()
    database = Database('new_Timesheet.db')
    acursor = database.acursor

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

    emp_record = Timestamp(rootWindow, database)

    # todo migrating everything onto the modular database.

    rootWindow.mainloop()
