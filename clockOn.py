import tkinter
import tkinter.ttk
import datetime
import sqlite3
db = sqlite3.connect('Timesheet.db')
acursor = db.cursor()



def get_current_time():
    cur_time = datetime.datetime.now().strftime('%H:%M')
    return cur_time


def get_current_date():
    cur_date = datetime.datetime.now().strftime('%d-%b-%Y')
    return cur_date


# todo CHECK empid + date existing in record ( since only one clock in a day)


class Timestamp:

    def __init__(self, window, clock_in=None, clock_out=None, name=None, date=None):
        self.clock_in = clock_in
        self.clock_out = clock_out
        self.employee_list = []
        self.date = date

        # status of an employee for current day, if they have clocked on/off or at all.
        self.clock_on_status = None
        self.clock_off_status = None
        self.date_status = None

        self.get_emp_list()

        # Construct the Option menu and populate it with employees
        self.emp_options = tkinter.ttk.Combobox(window, values=self.employee_list, state='readonly')
        self.emp_options.grid(row=1, column=1, columnspan=2, sticky='new')
        # Event(the box item being clicked) assigned to a handler(function get_employee).
        self.emp_options.bind('<<ComboboxSelected>>', self.emp_select)

        # Clock on and off buttons
        self.clock_on = tkinter.ttk.Button(window, text='Clock On', command=self.emp_clock_in)
        self.clock_on.grid(row=2, column=1, sticky='nw')

        self.clock_off = tkinter.ttk.Button(window, text='Clock Off', command=self.emp_clock_out)
        self.clock_off.grid(row=3, column=1, sticky='nw')


        self.emp_options.current(0)
        self.name = self.emp_options.get()
        print('is this running')
        print(self.name)
        print('is this running')
        self.status_update()

    # These status' check for clockin/clockout to see if it is empty.
    def status_update(self):
        # TODO Exception of when nothing is selected. This occurs when the program is freshly launched
        emp_id = self.get_emp_id()
        self.clock_on_status = acursor.execute('SELECT clock_on FROM timestamp WHERE emp_id=?', (emp_id,)).fetchone()
        self.clock_off_status = acursor.execute('SELECT clock_off FROM timestamp WHERE emp_id=?', (emp_id,)).fetchone()
        # todo need to compare current date with the max(timestamp.date)
        # todo datestatus TRUE -> clocked on today. FALSE havent clocked on and clock on needs to be enabled
        latest_date = acursor.execute('SELECT MAX(date) FROM timestamp WHERE emp_id=?', (emp_id,)).fetchone()[0]
        # print(get_current_date())
        # print(latest_date)
        # print(get_current_date() == latest_date)
        if get_current_date() == latest_date:

            self.date_status = True
        else:

            self.date_status = None

        self.user_status(self.clock_on_status, self.clock_off_status, self.date_status)

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
        acursor.execute('UPDATE timestamp SET clock_off = ? WHERE (emp_id = ? AND date = ?)',
                        (get_current_time(), self.get_emp_id(), get_current_date()))
        db.commit()
        self.status_update()

    def get_emp_id(self):
        sql_get_id = "SELECT emp_id FROM employee WHERE name=?"
        emp_id = acursor.execute(sql_get_id, (self.name,)).fetchone()[0]
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


    def get_emp_list(self):
        for row in acursor.execute("SELECT name FROM employee").fetchall():
            self.employee_list.append(row[0])


if __name__ == '__main__':


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

    emp_record = Timestamp(rootWindow)






    rootWindow.mainloop()
