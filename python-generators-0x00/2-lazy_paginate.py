import mysql.connector

def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="Damaris",
        password="......",
        database="ALX_prodev"
    )

def paginate_users(page_size, offset):
    """
    Fetch a page of users starting from `offset`, limited by `page_size`.
    Returns a list of user dicts.
    """
    conn = connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def lazy_paginate(page_size):
    """
    Generator that lazily fetches pages of user data.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        for user in page:
            yield user
        offset += page_size

# Example usage:
if __name__ == "__main__":
    for user in lazy_paginate(100):
        print(user)
