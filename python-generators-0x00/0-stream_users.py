def stream_users():
    connection = mysql.connector.connect(
        host="localhost",
        user="Damaris",
        password="Dama@5323",
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        print("Yielding row:", row)  # Add this line
        yield row

    cursor.close()
    connection.close()
