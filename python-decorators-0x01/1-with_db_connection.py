import sqlite3 
import functools
 
def with_db_connection(func): 
    @functools.wraps (func)
    def wrapper(*args, **kwargs):
            con=sqlite3.connect ("users.db")
            try:
                  results = func(con,*args, **kwargs)
                  return results
            finally:
                  con.close()
    return wrapper



@with_db_connection 
def get_user_by_id(conn, user_id): 
      cursor = conn.cursor() 
     # cursor.execute("INSERT INTO users(id,name,email)VALUES(?,?,?)"(1,"Gillian","gillian@gmail.com"))
      cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
      return cursor.fetchone() 
#### Fetch user by ID with automatic connection handling 
@with_db_connection
def create_user(con):
      cursor=con.cursor()
      cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
    ''')
      cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (?, ?, ?)", 
                  (2, "Gillian", "gil@example.com"))
      con.commit()
      con.close()

user2=create_user()    
user = get_user_by_id(user_id=2)
print(user)