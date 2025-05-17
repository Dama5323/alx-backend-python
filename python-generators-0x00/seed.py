import uuid
import mysql.connector
import csv

def connect_to_mysql():
    # Connect to MySQL server (without specifying a database)
    connection = mysql.connector.connect(
        host="localhost",
        user="Damaris",
        password="Dama@5323"
    )
    return connection

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

def connect_to_prodev():
    # Connect to the specific ALX_prodev database
    connection = mysql.connector.connect(
        host="localhost",
        user="Damaris",
        password="Dama@5323",
        database="ALX_prodev"
    )
    return connection

def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        INDEX(user_id)
    )
    """
    cursor.execute(create_table_query)
    cursor.close()

def insert_data(connection, csv_file):
    cursor = connection.cursor()

    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_id = str(uuid.uuid4())  # Generate a UUID for each user
            insert_query = """
            INSERT IGNORE INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (user_id, row['name'], row['email'], row['age']))

    connection.commit()
    cursor.close()

if __name__ == "__main__":
    conn = connect_to_mysql()
    create_database(conn)
    conn.close()

    conn = connect_to_prodev()
    create_table(conn)
    insert_data(conn, 'user_data.csv')
    conn.close()

    print("Database setup and data insertion complete!")
