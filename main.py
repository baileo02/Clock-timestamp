from tkinter.ttk import Notebook
import tkinter
from clockOn import *
from amend_timesheet import *
from display_timesheet import *
import sqlite3


class Main:

    def __init__(self):
        self.nb = Notebook(rootWindow)
        self.nb.pack()

        clock_frame = tkinter.Frame(self.nb)
        self.nb.add(clock_frame, text='Clock in')

        alter_frame = tkinter.Frame(self.nb)
        self.nb.add(alter_frame, text='Alter hours')

        display_frame = tkinter.Frame(self.nb)
        self.nb.add(display_frame, text='Display hours')

        display_sheet = DisplayGrid(display_frame)
        alter_sheet = AlterHours(alter_frame)
        clock_in = Timestamp(clock_frame)





db = sqlite3.connect('Timesheet.db')
acursor = db.cursor()
rootWindow = tkinter.Tk()
rootWindow.geometry('600x600')

app = Main()

rootWindow.mainloop()


