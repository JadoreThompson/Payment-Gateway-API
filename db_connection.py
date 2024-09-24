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
    conn = await asyncpg.connect(
        dsn=f"postgresql://{os.getenv('DB_USER')}:{quote(os.getenv('DB_PASSWORD'))}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    )

    await conn.execute('''\
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            email VARCHAR UNIQUE NOT NULL,
            phone VARCHAR(13) UNIQUE NOT NULL,
            business_type VARCHAR(50) NOT NULL,
            first_name VARCHAR NOT NULL,
            last_name VARCHAR NOT NULL,
            password VARCHAR NOT NULL,
            stripe_account_id VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    print(f"{create_tables.__name__}: Tables Created")


def run():
    asyncio.run(create_tables())



if __name__ == "__main__":
    run()
