# todo used to populate and test the database

import sqlite3

db = sqlite3.connect('Timesheet.db')
acursor = db.cursor()

# acursor.execute('DELETE FROM employee')
# acursor.execute('INSERT INTO employee (name) VALUES (?)', ('Bailey',))
# acursor.execute('INSERT INTO employee (name) VALUES (?)', ('Vivian',))
# acursor.execute('INSERT INTO employee (name) VALUES (?)', ('Elaine',))

acursor.execute('DELETE FROM timestamp')


acursor.execute('INSERT INTO timestamp (clock_on, clock_off, emp_id, date) VALUES (?,?,?,?)', ('10:32', '15:00', 6, '08-Jun-2020'))
acursor.execute('INSERT INTO timestamp (clock_on, clock_off, emp_id, date) VALUES (?,?,?,?)', ('10:32', '15:00', 6, '09-Jun-2020'))
acursor.execute('INSERT INTO timestamp (clock_on, clock_off, emp_id, date) VALUES (?,?,?,?)', ('10:32', '15:00', 6, '10-Jun-2020'))
acursor.execute('INSERT INTO timestamp (clock_on, emp_id, date) VALUES (?,?,?)', ('10:32', 6, '11-Jun-2020'))
acursor.execute('INSERT INTO timestamp (clock_on, clock_off, emp_id, date) VALUES (?,?,?,?)', ('10:32', '15:00', 6, '14-Jun-2020'))

acursor.execute('INSERT INTO timestamp (clock_on, clock_off, emp_id, date) VALUES (?,?,?,?)', ('10:32', '15:00', 7, '08-Jun-2020'))
acursor.execute('INSERT INTO timestamp (clock_on, clock_off, emp_id, date) VALUES (?,?,?,?)', ('10:32', '15:00', 7, '09-Jun-2020'))
acursor.execute('INSERT INTO timestamp (clock_on, clock_off, emp_id, date) VALUES (?,?,?,?)', ('10:32', '15:00', 7, '13-Jun-2020'))
acursor.execute('INSERT INTO timestamp (clock_on, clock_off, emp_id, date) VALUES (?,?,?,?)', ('10:32', '15:00', 7, '14-Jun-2020'))
acursor.execute('INSERT INTO timestamp (clock_on, emp_id, date) VALUES (?,?,?)', ('10:32', 7, '15-Jun-2020'))
acursor.execute('INSERT INTO timestamp (clock_on, emp_id, date) VALUES (?,?,?)', ('10:32', 7, '12-Jun-2020'))


acursor.execute('INSERT INTO timestamp (clock_on, clock_off, emp_id, date) VALUES (?,?,?,?)', ('10:32', '15:00', 8, '08-Jun-2020'))
acursor.execute('INSERT INTO timestamp (clock_on, clock_off, emp_id, date) VALUES (?,?,?,?)', ('10:32', '15:00', 8, '09-Jun-2020'))
acursor.execute('INSERT INTO timestamp (clock_on, clock_off, emp_id, date) VALUES (?,?,?,?)', ('10:32', '15:00', 8, '10-Jun-2020'))
acursor.execute('INSERT INTO timestamp (clock_on, clock_off, emp_id, date) VALUES (?,?,?,?)', ('10:32', '15:00', 8, '11-Jun-2020'))
acursor.execute('INSERT INTO timestamp (clock_on, clock_off, emp_id, date) VALUES (?,?,?,?)', ('10:32', '15:00', 8, '12-Jun-2020'))
acursor.execute('INSERT INTO timestamp (clock_on, clock_off, emp_id, date) VALUES (?,?,?,?)', ('10:32', '15:00', 8, '13-Jun-2020'))
acursor.execute('INSERT INTO timestamp (clock_on, clock_off, emp_id, date) VALUES (?,?,?,?)', ('10:32', '15:00', 8, '14-Jun-2020'))
acursor.execute('INSERT INTO timestamp (clock_on, clock_off, emp_id, date) VALUES (?,?,?,?)', ('10:32', '15:00', 8, '15-Jun-2020'))
acursor.execute('INSERT INTO timestamp (clock_on, clock_off, emp_id, date) VALUES (?,?,?,?)', ('10:32', '15:00', 8, '16-Jun-2020'))












db.commit()
