import asyncio
import aiosqlite
from datetime import datetime, timedelta

async def async_fetch_users(db_path):
    """Fetch all users from the database"""
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return users

async def async_fetch_older_users(db_path, age_threshold=40):
    """Fetch users older than the specified age threshold"""
    async with aiosqlite.connect(db_path) as db:
        query = "SELECT * FROM users WHERE age > ?"
        async with db.execute(query, (age_threshold,)) as cursor:
            users = await cursor.fetchall()
            return users

async def fetch_concurrently(db_path):
    """Run both queries concurrently using asyncio.gather"""
    users, older_users = await asyncio.gather(
        async_fetch_users(db_path),
        async_fetch_older_users(db_path)
    )
    return {
        "all_users": users,
        "older_users": older_users
    }

# Example usage
if __name__ == "__main__":
    # Create a test database (you would normally have this already)
    async def create_test_db():
        async with aiosqlite.connect("test.db") as db:
            await db.execute("DROP TABLE IF EXISTS users")
            await db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
            await db.executemany(
                "INSERT INTO users (name, age) VALUES (?, ?)",
                [("Alice", 35), ("Bob", 42), ("Charlie", 28), ("Diana", 45)]
            )
            await db.commit()
    
    # Run the example
    async def main():
        await create_test_db()
        results = await fetch_concurrently("test.db")
        print("All users:", results["all_users"])
        print("Users older than 40:", results["older_users"])
    
    asyncio.run(main())