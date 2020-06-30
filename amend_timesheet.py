from clockOn import employee_list, get_emp_list
import tkSimpleDialog
import sqlite3
import tkcalendar
import tkinter.ttk
from datetime import datetime
from tkinter import Button

db = sqlite3.connect('Timesheet.db')
acursor = db.cursor()
get_emp_list()


def tuple_check(atuple):
    if atuple:
        return atuple[0]
    else:
        return atuple


class AlterHours:

    def __init__(self, window):

        self.window = window

        self.selected_date = datetime.strftime(datetime.utcnow(), '%d-%b-%Y')
        # USER SELECTBOX

        emp_options = tkinter.ttk.Combobox(window, values=employee_list, state='readonly')
        emp_options.current(0)
        emp_options.grid(row=1, column=1, columnspan=2, sticky='nw')
        emp_options.bind('<<ComboboxSelected>>', self.employee_select)

        self.selected_employee = emp_options.get()

        # DATE SELECT
        datepicker = tkinter.Entry(window)
        datepicker.grid(row=2, column=1, sticky='nw')
        calender = tkcalendar.DateEntry(datepicker, locale='en_AU', date_pattern='dd-m-yy')
        calender.grid(row=0, column=1)
        calender.bind('<<DateEntrySelected>>', self.date_select)

        # CLOCK ON / OFF LABEL
        clock_on_label = tkinter.Label(window, text='Clock On ')
        clock_on_label.grid(row=3, column=1, sticky='nw')

        clock_off_label = tkinter.Label(window, text='Clock Off ')
        clock_off_label.grid(row=4, column=1, sticky='nw')

        # CLOCK ON / OFF TIME DISPLAY
        self.clock_on_time = tkinter.Button(window, text='None', command=self.set_clock_on)
        self.clock_on_time.grid(row=3, column=2, sticky='nw')

        self.clock_off_time = tkinter.Button(window, text='None', command=self.set_clock_off)
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
        # logic to decide time to update.
        self.check_clock(change_clock_on, time)
        self.update_time()
        db.commit()

    def check_clock(self, change_clock_on, time):
        emp_id = self.get_emp_id(self.selected_employee)[0]
        clock_on_time = acursor.execute('SELECT clock_on FROM timestamp WHERE (emp_id=? AND date=?)',
                                        (emp_id, self.selected_date)).fetchone()
        clock_off_time = acursor.execute('SELECT clock_off FROM timestamp WHERE (emp_id=? AND date=?)',
                                         (emp_id, self.selected_date)).fetchone()
        # if on and off both have values
        if tuple_check(clock_on_time) and tuple_check(clock_off_time):
            print('run0')
            if change_clock_on:
                if time <= clock_off_time[0]:
                    self.alter_clock_execute(time, 'clock_on')
                else:
                    print('ON must be earlier than OFF')
            else:
                if time >= clock_on_time[0]:
                    self.alter_clock_execute(time, 'clock_off')
                else:
                    print('OFF must be greater than ON')
        # if on and off are both NONE, basically inserting an entire row of record
        elif not tuple_check(clock_on_time):
            if not tuple_check(clock_off_time):
                # check which time to change.
                if change_clock_on:
                    self.insert_record('clock_on', time, emp_id, self.selected_date)
                else:
                    self.insert_record('clock_off', time, emp_id, self.selected_date)
            else:
                # if clock on time is NONE but clock off time exists
                print('run3')
                if change_clock_on:
                    if time <= clock_off_time[0]:
                        self.alter_clock_execute(time, 'clock_on')
                    else:
                        print('On must be less than OFF')
                else:
                    self.alter_clock_execute(time, 'clock_off')
        else:
            print('run2')
            # if clock on time exists but clock off doesnt.
            if change_clock_on:
                self.alter_clock_execute(time, 'clock_on')
            else:
                if time >= clock_on_time[0]:
                    self.alter_clock_execute(time, 'clock_off')

    def insert_record(self, column, time, emp_id, date):
        sql_insert_record = "INSERT INTO timestamp ({}, emp_id, date) VALUES (?, ?, ?)".format(column)
        acursor.execute(sql_insert_record, (time, emp_id, date))
        db.commit()
        self.update_time()

    def alter_clock_execute(self, altered_time, column):
        sql_change_time = "UPDATE timestamp SET {0} = ? WHERE (emp_id=? AND date=?)".format(column)
        acursor.execute(sql_change_time,
                        (altered_time, self.get_emp_id(self.selected_employee)[0], self.selected_date))
        db.commit()
        self.update_time()

    def update_time(self):
        self.clock_on_time['text'] = self.show_clock(True)[0]
        self.clock_off_time['text'] = self.show_clock(False)[1]

    def set_clock_on(self):
        # clock_on = ClockOn(self.window)
        self.dialogWindow = tkinter.Toplevel(self.window)
        self.timepicker_frame = tkinter.Frame(self.dialogWindow)
        self.timepicker_frame.grid(row=0, column=0)
        self.hourSpinner = tkinter.Spinbox(self.timepicker_frame, width=2, state='readonly', values=tuple(range(0, 24)))
        self.minuteSpinner = tkinter.Spinbox(self.timepicker_frame, width=2, from_=0, to=59, state='readonly')
        self.hourSpinner.grid(row=0, column=0, sticky='w')
        self.minuteSpinner.grid(row=0, column=2)
        tkinter.Label(self.timepicker_frame, text='Hr').grid(row=0, column=1, sticky='e')
        tkinter.Label(self.timepicker_frame, text='Min').grid(row=0, column=3, sticky='e')
        self.dialogWindow.geometry("+%d+%d" % (self.window.winfo_rootx()+50,
                                  self.window.winfo_rooty()+50))

        self.box = tkinter.Frame(self.dialogWindow)
        self.box.grid(row=1, column=0)
        w = Button(self.box, text="SET", width=10, command=self.on_ok)
        w.grid(row=1, column=0)
        w = Button(self.box, text="Cancel", width=10, command=self.on_cancel)
        w.grid(row=1, column=2)

        self.dialogWindow.wait_window()

    def on_ok(self):

        self.dialogWindow.withdraw()
        self.dialogWindow.update_idletasks()
        self.alter_clock(self.hourSpinner.get(), self.minuteSpinner.get(), True)
        self.on_cancel()


    def on_cancel(self):
        self.dialogWindow.focus_set()
        self.dialogWindow.destroy()


    def set_clock_off(self):
        self.dialogWindow = tkinter.Toplevel(self.window)
        self.timepicker_frame = tkinter.Frame(self.dialogWindow)
        self.timepicker_frame.grid(row=0, column=0)
        self.hourSpinner = tkinter.Spinbox(self.timepicker_frame, width=2, state='readonly', values=tuple(range(0, 24)))
        self.minuteSpinner = tkinter.Spinbox(self.timepicker_frame, width=2, from_=0, to=59, state='readonly')
        self.hourSpinner.grid(row=0, column=0, sticky='w')
        self.minuteSpinner.grid(row=0, column=2)
        tkinter.Label(self.timepicker_frame, text='Hr').grid(row=0, column=1, sticky='e')
        tkinter.Label(self.timepicker_frame, text='Min').grid(row=0, column=3, sticky='e')

        self.dialogWindow.geometry("+%d+%d" % (self.window.winfo_rootx()+50,
                                               self.window.winfo_rooty()+50))
        self.box = tkinter.Frame(self.dialogWindow)
        self.box.grid(row=1, column=0)
        w = Button(self.box, text="SET", width=10, command=self.off_ok)
        w.grid(row=1, column=0)
        w = Button(self.box, text="Cancel", width=10, command=self.off_cancel)
        w.grid(row=1, column=2)

        self.dialogWindow.wait_window()

    def off_ok(self):

        self.dialogWindow.withdraw()
        self.dialogWindow.update_idletasks()
        self.alter_clock(self.hourSpinner.get(), self.minuteSpinner.get(), False)
        self.off_cancel()


    def off_cancel(self):
        self.dialogWindow.focus_set()
        self.dialogWindow.destroy()


# class ClockOn(tkSimpleDialog.Dialog):
#     def body(self, master):
#         # TIME PICKER
#         timepicker_frame = tkinter.Frame(master)
#         timepicker_frame.grid(row=0, column=0)
#         self.hourSpinner = tkinter.Spinbox(timepicker_frame, width=2, state='readonly', values=tuple(range(0, 24)))
#         self.minuteSpinner = tkinter.Spinbox(timepicker_frame, width=2, from_=0, to=59, state='readonly')
#         self.hourSpinner.grid(row=0, column=0, sticky='w')
#         self.minuteSpinner.grid(row=0, column=2)
#         tkinter.Label(timepicker_frame, text='Hr').grid(row=0, column=1, sticky='e')
#         tkinter.Label(timepicker_frame, text='Min').grid(row=0, column=3, sticky='e')
#         return self.hourSpinner
#
#     def apply(self):
#
#         alter.alter_clock(self.hourSpinner.get(), self.minuteSpinner.get(), True)
#
# class ClockOff(tkSimpleDialog.Dialog):
#     def body(self, master):
#         # TIME PICKER
#         timepicker_frame = tkinter.Frame(master)
#         timepicker_frame.grid(row=0, column=0)
#         self.hourSpinner = tkinter.Spinbox(timepicker_frame, width=2, state='readonly', values=tuple(range(0, 24)))
#         self.minuteSpinner = tkinter.Spinbox(timepicker_frame, width=2, from_=0, to=59, state='readonly')
#         self.hourSpinner.grid(row=0, column=0, sticky='w')
#         self.minuteSpinner.grid(row=0, column=2)
#         tkinter.Label(timepicker_frame, text='Hr').grid(row=0, column=1, sticky='e')
#         tkinter.Label(timepicker_frame, text='Min').grid(row=0, column=3, sticky='e')
#         return self.hourSpinner
#
#     def apply(self):
#         # alter.alter_clock(self.hourSpinner.get(), self.minuteSpinner.get(), False)
#         self.hourSpinner.get(), self.minuteSpinner.get(), False


if __name__ == '__main__':

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
    alter = AlterHours(root)

    root.mainloop()
