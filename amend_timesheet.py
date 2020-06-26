from clockOn import employee_list, get_emp_list
import tkSimpleDialog
import sqlite3
import tkcalendar
import tkinter.ttk
from datetime import datetime

db = sqlite3.connect('Timesheet.db')
acursor = db.cursor()
get_emp_list()


class AlterHours:

    def __init__(self):


        self.selected_date = datetime.strftime(datetime.utcnow(), '%d-%b-%Y')
        # USER SELECTBOX

        emp_options = tkinter.ttk.Combobox(root, values=employee_list, state='readonly')
        emp_options.current(0)
        emp_options.grid(row=1, column=1, columnspan=2, sticky='nw')
        emp_options.bind('<<ComboboxSelected>>', self.employee_select)

        self.selected_employee = emp_options.get()

        # DATE SELECT
        datepicker = tkinter.Entry(root)
        datepicker.grid(row=2, column=1, sticky='nw')
        calender = tkcalendar.DateEntry(datepicker, locale='en_AU', date_pattern='dd-m-yy')
        calender.grid(row=0, column=1)
        calender.bind('<<DateEntrySelected>>', self.date_select)

        # CLOCK ON / OFF LABEL
        clock_on_label = tkinter.Label(root, text='Clock On ')
        clock_on_label.grid(row=3, column=1, sticky='nw')

        clock_off_label = tkinter.Label(root, text='Clock Off ')
        clock_off_label.grid(row=4, column=1, sticky='nw')

        # CLOCK ON / OFF TIME DISPLAY
        self.clock_on_time = tkinter.Button(root, text='None', command=self.set_clock_on)
        self.clock_on_time.grid(row=3, column=2, sticky='nw')

        self.clock_off_time = tkinter.Button(root, text='None', command=self.set_clock_off)
        self.clock_off_time.grid(row=4, column=2, sticky='nw')

        self.update_time()


    def get_emp_id(self, employee_name):
        sql_get_id = "SELECT emp_id FROM employee WHERE name=?"
        emp_id = acursor.execute(sql_get_id, (employee_name,)).fetchone()
        return emp_id

    # EMPLOYEE SELECT
    def employee_select(self, event):
        self.selected_employee = event.widget.get()
        self.update_time()

    # DATE SELECT
    def date_select(self, event):
        selected_date = event.widget.get_date()
        self.selected_date = datetime.strftime(selected_date, '%d-%b-%Y')
        self.update_time()

    def show_clock(self, on=True):
        # SHOW CLOCK ON / CLOCK OFF TIMES GIVEN DATE AND EMPLOYEE
        sql_clockon = "SELECT clock_on FROM timestamp WHERE (emp_id=? AND date=?)"
        sql_clockoff = "SELECT clock_off FROM timestamp WHERE (emp_id=? AND date=?)"
        emp_id = self.get_emp_id(self.selected_employee)[0]
        clock_on = acursor.execute(sql_clockon, (emp_id, self.selected_date)).fetchone()
        clock_off = acursor.execute(sql_clockoff, (emp_id, self.selected_date)).fetchone()
        if clock_on:
            if clock_off[0]:
                return clock_on, clock_off
            else:
                return clock_on, 'None'
        else:
            return 'None', 'None'

    def alter_clock(self, hour, minute, change_clock_on):
        # ALTER THE CLOCK ON/ CLOCK OFF DATES
        time = (hour.zfill(2) + ':' + minute.zfill(2))
        alter_clock_on = time
        alter_clock_off = time
        # logic to decide time to update.
        self.check_clock(change_clock_on, alter_clock_on, alter_clock_off)
        self.update_time()
        db.commit()

    def check_clock(self, change_clock_on, alter_clock_on, alter_clock_off):
        emp_id = self.get_emp_id(self.selected_employee)[0]
        if change_clock_on:
            if alter_clock_on <= (acursor.execute('SELECT clock_off FROM timestamp WHERE (emp_id=? AND date=?)',
                                                  (emp_id, self.selected_date)).fetchone())[0]:
                print(alter_clock_on)
                print((acursor.execute('SELECT clock_off FROM timestamp WHERE (emp_id=? AND date=?)',
                                       (emp_id, self.selected_date)).fetchone())[0])
                sql_change_time = "UPDATE timestamp SET {0} = ? WHERE (emp_id=? AND date=?)".format('clock_on')
                acursor.execute(sql_change_time,
                                (alter_clock_on, self.get_emp_id(self.selected_employee)[0], self.selected_date))
            else:
                print('clock on time must be behind clock off time')
        else:
            if alter_clock_off >= (acursor.execute('SELECT clock_on FROM timestamp WHERE (emp_id=? AND date=?)',
                                                   (emp_id, self.selected_date)).fetchone())[0]:
                sql_change_time = "UPDATE timestamp SET {0} = ? WHERE (emp_id=? AND date=?)".format('clock_off')
                acursor.execute(sql_change_time,
                                (alter_clock_off, self.get_emp_id(self.selected_employee)[0], self.selected_date))
            else:
                print('clock off time must be ahead of clock on time')

    def update_time(self):
        self.clock_on_time['text'] = self.show_clock(True)[0]
        self.clock_off_time['text'] = self.show_clock(False)[1]

    def set_clock_on(self):
        clock_on = ClockOn(root)

    def set_clock_off(self):
        clock_off = ClockOff(root)


class ClockOn(tkSimpleDialog.Dialog):
    def body(self, master):
        # TIME PICKER
        timepicker_frame = tkinter.Frame(master)
        timepicker_frame.grid(row=0, column=0)
        self.hourSpinner = tkinter.Spinbox(timepicker_frame, width=2, state='readonly', values=tuple(range(0, 24)))
        self.minuteSpinner = tkinter.Spinbox(timepicker_frame, width=2, from_=0, to=59, state='readonly')
        self.hourSpinner.grid(row=0, column=0, sticky='w')
        self.minuteSpinner.grid(row=0, column=2)
        tkinter.Label(timepicker_frame, text='Hr').grid(row=0, column=1, sticky='e')
        tkinter.Label(timepicker_frame, text='Min').grid(row=0, column=3, sticky='e')
        return self.hourSpinner

    def apply(self):
        alter.alter_clock(self.hourSpinner.get(), self.minuteSpinner.get(), True)


class ClockOff(tkSimpleDialog.Dialog):
    def body(self, master):
        # TIME PICKER
        timepicker_frame = tkinter.Frame(master)
        timepicker_frame.grid(row=0, column=0)
        self.hourSpinner = tkinter.Spinbox(timepicker_frame, width=2, state='readonly', values=tuple(range(0, 24)))
        self.minuteSpinner = tkinter.Spinbox(timepicker_frame, width=2, from_=0, to=59, state='readonly')
        self.hourSpinner.grid(row=0, column=0, sticky='w')
        self.minuteSpinner.grid(row=0, column=2)
        tkinter.Label(timepicker_frame, text='Hr').grid(row=0, column=1, sticky='e')
        tkinter.Label(timepicker_frame, text='Min').grid(row=0, column=3, sticky='e')
        return self.hourSpinner

    def apply(self):
        alter.alter_clock(self.hourSpinner.get(), self.minuteSpinner.get(), False)


# CONFIGURE DISPLAY
root = tkinter.Tk()
root.geometry('300x300')

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=3)
root.columnconfigure(3, weight=5)
root.columnconfigure(4, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=1)
root.rowconfigure(5, weight=3)
# Initialize AlterHour
alter = AlterHours()

root.mainloop()

