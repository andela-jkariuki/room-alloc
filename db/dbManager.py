import sqlite3 as lite

class DBManager:
    """Create a new connection to the sqlite database"""
    def __init__(self, db_name):
        self.connection = lite.connect(db_name)
        self.cursor = self.connection.cursor()

        self.migrations()

    def migrations(self):
        """
        Create the tables if they do not exist
        """
        with self.connection:
            self.cursor.executescript("""
                CREATE TABLE IF NOT EXISTS rooms (
                    id    INTEGER PRIMARY KEY AUTOINCREMENT,
                    name  INTEGER UNIQUE,
                    type  CHAR(1)
                );
                """)

    def run_many_queries(self, query_string, data):
        """
        Run the executemany command to query multiple statements
        """
        try:
            with self.connection:
                self.cursor.executemany(query_string, data)
                return True
        except lite.IntegrityError:
            return False