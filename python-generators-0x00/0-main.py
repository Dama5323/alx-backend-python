# 0-main.py

import seed

connection = seed.connect_to_prodev()
seed.create_database(connection)
connection.close()

print("connection successful")
