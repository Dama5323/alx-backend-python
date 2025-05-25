import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=()):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print("Database connection opened.")
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")


# Setup test database
def setup_db():
    conn = sqlite3.connect("my_database.db")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    users = [
        ('Alice', 24),
        ('Bob', 30),
        ('Charlie', 28),
        ('Diana', 22)
    ]
    cur.executemany("INSERT INTO users (name, age) VALUES (?, ?)", users)
    conn.commit()
    conn.close()

# Main usage
if __name__ == "__main__":
    setup_db()

    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery("my_database.db", query, params) as results:
        for row in results:
            print(row)
