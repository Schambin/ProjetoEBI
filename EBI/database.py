import sqlite3

class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cpf (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpf TEXT UNIQUE
            )
        ''')
        self.connection.commit()

    def insert_cpf(self, cpf):
        try:
            self.cursor.execute('INSERT INTO cpf (cpf) VALUES (?)', (cpf,))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def check_cpf(self, cpf):
        self.cursor.execute('SELECT EXISTS (SELECT 1 FROM cpf WHERE cpf = ?)', (cpf,))
        return self.cursor.fetchone()[0] == 1

    def close(self):
        self.connection.close()
