import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="Damaris",
    password="Dama@5323",
    database="ALX_prodev"
)

cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM user_data")
count = cursor.fetchone()[0]
print(f"Total rows in user_data: {count}")
cursor.close()
conn.close()
