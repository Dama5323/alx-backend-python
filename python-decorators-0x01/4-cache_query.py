import time
import sqlite3 
import functools

query_cache = {}

# Assume with_db_connection is already defined
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Cache decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Try to extract the query (assumed to be a keyword arg or second positional arg)
        query = kwargs.get('query') or (args[1] if len(args) > 1 else None)

        if query in query_cache:
            print("Returning cached result for query.")
            return query_cache[query]

        print("Executing and caching result for query.")
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
