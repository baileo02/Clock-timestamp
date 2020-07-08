from tkinter.ttk import Notebook
import tkinter
from clockOn import *
from amend_timesheet import *
from display_timesheet import *
import sqlite3
from database_connection import Database
from babel.numbers import *





class Main:

    def __init__(self):
        self.nb = Notebook(rootWindow)
        self.nb.pack()

        database = Database('new_Timesheet.db')


        clock_frame = tkinter.Frame(self.nb)
        self.nb.add(clock_frame, text='Clock in')
        display_frame = tkinter.Frame(self.nb)
        self.nb.add(display_frame, text='Display hours')

        alter_frame = tkinter.Frame(self.nb)
        self.nb.add(alter_frame, text='Alter hours')


        display_sheet = DisplayGrid(display_frame, database)
        alter_sheet = AlterHours(alter_frame, database)
        clock_in = Timestamp(clock_frame, database)


        #todo when switching tabs, it should update one another.
        #todo clock on time label should change dynamically with changing users.




rootWindow = tkinter.Tk()
rootWindow.geometry('500x300')
app = Main()
rootWindow.mainloop()


