import asyncio
import aiosqlite

async def async_fetch_users(db_path):
    """Fetch all users from the database"""
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return users

async def async_fetch_older_users(db_path):
    """Fetch users older than 40"""
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            users = await cursor.fetchall()
            return users

async def fetch_concurrently(db_path):
    """Run both queries concurrently"""
    users, older_users = await asyncio.gather(
        async_fetch_users(db_path),
        async_fetch_older_users(db_path)
    )
    return users, older_users

if __name__ == "__main__":
    async def main():
        # Example usage
        db_path = "example.db"
        # Create test database (in a real scenario, this would exist)
        async with aiosqlite.connect(db_path) as db:
            await db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
            await db.execute("INSERT INTO users (name, age) VALUES ('Alice', 35), ('Bob', 45), ('Charlie', 28), ('Diana', 50)")
            await db.commit()
        
        # Run concurrent queries
        all_users, older_users = await fetch_concurrently(db_path)
        print("All users:", all_users)
        print("Users older than 40:", older_users)

    asyncio.run(main())