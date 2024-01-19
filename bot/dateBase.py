import sqlite3


class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.initialize_database()

    def initialize_database(self):
        with self.connection:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS status(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    status TEXT
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS task(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT,
                    status_ID INTEGER,
                    FOREIGN KEY (status_ID) REFERENCES status(ID)
                )
            ''')
            self.cursor.execute('''
                INSERT OR IGNORE INTO status (status) VALUES ('виконано'), ('не виконано')
            ''')

    def create_or_insert(self, task_name):
        with self.connection:
            self.cursor.execute(
                'INSERT INTO task (task, status_ID) VALUES (?, (SELECT ID FROM status WHERE status = ?))',
                (task_name, 'не виконано')
            )
            return self.cursor.lastrowid

    def get_all_id(self):
        with self.connection:
            result = self.cursor.execute('SELECT ID FROM task').fetchall()
            return [row[0] for row in result]

    def get_all_tasks(self):
        with self.connection:
            result = self.cursor.execute('''
                SELECT task.ID, task.task, status.status 
                FROM task 
                JOIN status ON task.status_ID = status.ID
            ''').fetchall()
            return result

    def mark_completed(self, task_id: int):
        try:
            with self.connection:
                self.cursor.execute(
                    'UPDATE task SET status_ID = (SELECT ID FROM status WHERE status = "виконано") WHERE ID = ?',
                    (task_id,)
                )
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False

        return True

    def edit_task_title(self, task_id: int, new_title: str):
        try:
            with self.connection:
                self.cursor.execute('UPDATE task SET task = ? WHERE ID = ?', (new_title, task_id))
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False

        return True

    def delete_task(self, task_id: int):
        try:
            with self.connection:
                self.cursor.execute('DELETE FROM task WHERE ID = ?', (task_id,))

                self.cursor.execute('UPDATE task SET ID = ID - 1 WHERE ID > ?', (task_id,))
        except sqlite3.Error as e:
            print(f"Помилка SQLite: {e}")
            return False

        return True
