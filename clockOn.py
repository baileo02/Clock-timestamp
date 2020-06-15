import tkinter
import tkinter.ttk


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

# Employee user list. This is temporary and should be populated by the database instead #
emplist = ['bailey', 'vivian', 'elaine']        #todo replace with database



# Construct the Option menu and populate it with employees
emp_options = tkinter.ttk.Combobox(rootWindow, values=emplist, state='readonly')
emp_options.grid(row=1, column=1, columnspan=2, sticky='new')


# Clock on and off buttons
clock_on = tkinter.ttk.Button(rootWindow, text='Clock On')
clock_on.grid(row=2, column=1, sticky='nw')

clock_off = tkinter.ttk.Button(rootWindow, text='Clock Off')
clock_off.grid(row=3, column=1, sticky='nw')






rootWindow.mainloop()
