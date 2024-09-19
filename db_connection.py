import asyncio
import os
from dotenv import load_dotenv
import asyncpg
from contextlib import asynccontextmanager
from pathlib import Path

load_dotenv(f"{Path(__file__).parent}/.env")


@asynccontextmanager
async def get_connection():
    conn = await asyncpg.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"),
                                 database=os.getenv("DB_NAME"), host=os.getenv("DB-HOST"))
    try:
        yield conn
    finally:
        if conn:
            await conn.close()


async def create_tables():
    async with get_connection() as conn:
        await conn.execute("""\
            CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                email VARCHAR(20) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                fname VARCHAR(20) NOT NULL
            );    
        """)


def run():
    asyncio.run(create_tables())


run()
