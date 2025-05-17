import mysql.connector

def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="Damaris",
        password="....",
        database="ALX_prodev"
    )

def stream_user_ages():
    """
    Generator that yields user ages one by one.
    """
    conn = connect_to_prodev()
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:
        yield age

    cursor.close()
    conn.close()

def calculate_average_age():
    """
    Calculates the average age using the stream_user_ages generator.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")

if __name__ == "__main__":
    calculate_average_age()
