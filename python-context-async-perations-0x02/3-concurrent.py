import asyncio
import aiosqlite

async def async_fetch_users():
    async with aiosqlite.connect("example.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

async def async_fetch_older_users():
    async with aiosqlite.connect("example.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            return await cursor.fetchall()

async def fetch_concurrently():
    return await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    async def create_test_db():
        async with aiosqlite.connect("example.db") as db:
            await db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
            await db.execute("INSERT INTO users (name, age) VALUES ('Alice', 35), ('Bob', 45), ('Charlie', 28), ('Diana', 50)")
            await db.commit()

    async def main():
        await create_test_db()
        users, older_users = await fetch_concurrently()
        print("All users:", users)
        print("Older users:", older_users)

    asyncio.run(main())