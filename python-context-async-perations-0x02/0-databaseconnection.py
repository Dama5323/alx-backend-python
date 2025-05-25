import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print("Database connection opened.")
        return self.cursor  # return the cursor to perform operations

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

# Demo usage
if __name__ == "__main__":
    # Set up the database and a sample 'users' table (if not already present)
    with sqlite3.connect("my_database.db") as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
        cur.execute("INSERT INTO users (name) VALUES ('Alice'), ('Bob'), ('Charlie')")
        conn.commit()

    # Use the custom context manager to query from the users table
    with DatabaseConnection("my_database.db") as db:
        db.execute("SELECT * FROM users")
        rows = db.fetchall()
        for row in rows:
            print(row)
