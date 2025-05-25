import asyncio
import aiosqlite

DB_NAME = "my_async_database.db"

# Setup DB with sample data
async def setup_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DROP TABLE IF EXISTS users")
        await db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        await db.executemany(
            "INSERT INTO users (name, age) VALUES (?, ?)",
            [
                ('Alice', 24),
                ('Bob', 45),
                ('Charlie', 35),
                ('Diana', 50)
            ]
        )
        await db.commit()

# Async function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("All Users:")
            for user in users:
                print(user)

# Async function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            print("\nUsers Older Than 40:")
            for user in older_users:
                print(user)

# Run both queries concurrently
async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# Entry point
if __name__ == "__main__":
    asyncio.run(setup_db())
    asyncio.run(fetch_concurrently())
