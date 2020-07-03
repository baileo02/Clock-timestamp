import sqlite3

class Database:

    def __init__(self, db_file):
        self.db_file = db_file
        self.acursor = None

        self.db = None
        self.create_connection(db_file)

    def create_connection(self, db_file):
        try:
            self.db = sqlite3.connect(db_file)
            self.acursor = self.db.cursor()
            self.create_tables()
            # self.insert_employees() # todo remove
            self.db.commit()
        except sqlite3.Error as e:
            print(e)


    def create_tables(self):
        if self.acursor:
            self.acursor.execute('CREATE TABLE IF NOT EXISTS employee (emp_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT NOT NULL)')
            self.acursor.execute('CREATE TABLE IF NOT EXISTS timestamp (clock_on TEXT, clock_off TEXT, emp_id INTEGER NOT NULL, date TEXT, record_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE)')

    def insert_employees(self):
        if self.acursor:
            self.acursor.execute('INSERT OR IGNORE INTO employee (name) VALUES ("Bailey")')
            self.acursor.execute('INSERT OR IGNORE INTO employee (name) VALUES ("Vivian")')
            self.acursor.execute('INSERT OR IGNORE INTO employee (name) VALUES ("Elaine")')





if __name__ == '__main__':
    database = Database('timesheet2.db')
