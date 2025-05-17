import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that yields user_data in batches of 'batch_size'.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="Damaris",
            password="Dama@5323",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) as total FROM user_data")
        total_rows = cursor.fetchone()['total']

        for offset in range(0, total_rows, batch_size):
            cursor.execute(
                "SELECT * FROM user_data LIMIT %s OFFSET %s", (batch_size, offset)
            )
            batch = cursor.fetchall()
            yield batch

        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return

def batch_processing(batch_size):
    """
    Processes batches to yield users over the age of 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if float(user['age']) > 25:
                yield user
