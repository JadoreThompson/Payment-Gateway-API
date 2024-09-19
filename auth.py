from db_connection import get_connection
from Resources.models import (
    SignUpBody,
    User
)

# FastAPI
from fastapi import APIRouter
from fastapi.responses import JSONResponse


# Functions
async def check_existing_user(conn, email) -> bool:
    row = await conn.fetchrow('''
                SELECT 1 FROM users WHERE email = $1
            ''', email)
    if row:
        return True
    return False


def generate_cols_and_placeholders(data: dict):
    cols = [key for key in data if data[key]]
    placeholders = ", ".join([f"${i + 1}" for i in range(0, len(cols))])
    values = [data[key] for key in cols]
    return ", ".join(cols), placeholders, values


def print_exception(func_name, e):
    print(f"{func_name}: {type(e).__name__} - {str(e)}")


# Initialisation
auth = APIRouter(prefix="/auth", tags=["auth"])


@auth.post("/signup")
async def signup(user: SignUpBody):
    async with get_connection() as conn:
        try:
            if await check_existing_user(conn, user.email):
                return JSONResponse(status_code=409, content={"message": "User already exists"})

            # Inserting User to DB
            cols, placeholders, values = generate_cols_and_placeholders(user.dict())
            row = await conn.fetchrow(f'''
                INSERT INTO users ({cols}) VALUES({placeholders}) RETURNING id
            ''', *values)

            if row:
                return JSONResponse(status_code=200,
                                    content={"message": "Successfully Signed Up", "user_id": row["id"]})
            return JSONResponse(status_code=501, content={"message": "Something went wrong. Please try again"})
        except Exception as e:
            print_exception(signup.__name__, e)
            return JSONResponse(status_code=500, content={"message": "Internal Server Error"})


@auth.post("/login")
async def login(user: User):
    async with get_connection() as conn:
        try:
            if await check_existing_user(conn, user.email):
                password = await conn.fetchrow('''
                    SELECT password FROM users WHERE email = $1
                ''', user.email)
                if user.password == password["password"]:
                    return JSONResponse(status_code=200, content={"message": "Successfully Logged In"})
                return JSONResponse(status_code=409, content={"message": "Invalid Credentials"})
            return JSONResponse(status_code=404, content={"message": "Invalid Credentials"})

        except Exception as e:
            print_exception(signup.__name__, e)
            return JSONResponse(status_code=500, content={"message": "Internal Server Error"})
