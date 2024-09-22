import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import quote

import os
from dotenv import load_dotenv

import asyncpg


load_dotenv(f"{Path(__file__).parent}/.env")
conn_pool = None


async def init_db_pool():
    global conn_pool
    conn_pool = await asyncpg.create_pool(
        dsn=f"postgresql://{os.getenv('DB_USER')}:{quote(os.getenv('DB_PASSWORD'))}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}",
        min_size=1,
        max_size=10
    )


async def close_db_pool():
    await conn_pool.close()


@asynccontextmanager
async def get_connection():
    async with conn_pool.acquire() as conn:
        yield conn


async def create_tables():
    async with get_connection() as conn:
        await conn.execute('''\
            CREATE TABLE IF NOT EXISTS users(
                user_id SERIAL PRIMARY KEY,
                email VARCHAR(20) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                fname VARCHAR NOT NULL,
                sname VARCHAR NOT NULL
            );
        ''')
        print(f"{create_tables.__name__}: Tables Created")


def run():
    asyncio.run(create_tables())


if __name__ == "__main__":
    run()
