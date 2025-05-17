# 🐍 ALX Backend Python — Database Seeder & Row Streamer

## 📌 Overview

This project initializes a MySQL database (`ALX_prodev`) and a table (`user_data`) using data from a CSV file. Each user entry is assigned a unique UUID. The project also includes a Python generator that streams rows from the database one by one for efficient memory usage.

---

## 🚀 Features

- ✅ Connects to MySQL and creates the `ALX_prodev` database if it doesn't exist
- ✅ Creates the `user_data` table with the following fields:
  - `user_id` (UUID, Primary Key, Indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)
- ✅ Loads data from `user_data.csv`
- ✅ Assigns UUIDs to each user record
- ✅ Inserts data while avoiding duplicates
- ✅ Streams records using a Python generator

---

## 🛠️ Requirements

- Python 3.x
- MySQL Server installed and running
- Install dependencies via pip:

```bash
pip install mysql-connector-python

## File Structure

📁 python-generators-0x00/
├── seed.py            # Sets up database, table, inserts data
├── user_data.csv      # Contains user data: name, email, age
├── 0-main.py          # Optional file to test generator
└── README.md          # Project documentation

💡 Usage
Ensure user_data.csv is in the root directory.

Run the seeding script:
python seed.py
This will:

Connect to MySQL

Create the ALX_prodev database (if not exists)

Create the user_data table

Insert data from user_data.csv with generated UUIDs

🧪 Generator Function (Optional)
A generator function is provided to yield rows one by one from the user_data table:

def stream_user_data(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row
    cursor.close()
📝 Notes
Ensure the MySQL server is running and accessible.

Update the MySQL credentials in seed.py to match your local environment.

The script uses INSERT IGNORE to avoid duplicate user_id conflicts.

👩‍💻 Author
Developed as part of the ALX Backend Specialization

