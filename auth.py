from contextlib import asynccontextmanager
from typing import Tuple

from db_connection import get_connection
from models import (
LoginObject,
SignUpObject,
TokenCreateObject,
AccountObject
)
from tools import print_exception

import stripe

# FastAPI
from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse


# Important
''' Defaults
"requirement_collection": "application",
"fees": {"payer": "application"},
"losses": {"payments": "application"},
"stripe_dashboard": {"type": "none"}
'''


async def check_if_user_exists(cur, email) -> bool:
    if await cur.fetchrow('SELECT 1 FROM users WHERE email = $1', email):
        return True
    return False


def get_cols_and_placeholders(data) -> Tuple[str, str, list]:
    cols = [key for key in data if data[key]]
    placeholders = [f"${i}" for i in range(len(cols))]
    values = [(data[key]) for key in cols]
    return ", ".join(cols), ", ".join(placeholders), values


# Initialisation
auth = APIRouter(prefix="/auth", tags=["auth"])


@auth.post("/create-token")
async def create_token(token_obj: TokenCreateObject):
    try:
        created_token = stripe.Token.create(**token_obj.dict())
        return created_token
    except Exception as e:
        print_exception(create_token.__name__, e)
        return Exception(e)


@auth.post("/create-account")
async def create_account(account_obj: AccountObject, token):
    account = stripe.Account.create(
        country="GB",
        email="johnemal@gmail.com",
        account_token=token
    )
    return account


@auth.post('/signup')
async def signup(user: TokenCreateObject):
    async with get_connection() as conn:
        async with conn.cursor() as cur:
            try:
                if await check_if_user_exists(cur, user.email):
                    return JSONResponse(status_code=409, content={"message": "User already exists"})

                # TODO: Implement some sort of confirm email flow

                # Getting the secure token of the user's information
                signup_obj = SignUpObject(**user.dict(exclude={key for key in user.dict() if key not in [key for key in SignUpObject.__fields__]}))
                cols, placeholders, values = get_cols_and_placeholders(signup_obj.dict())

                if await cur.execute(f'INSERT INTO users({cols}) VALUES ({placeholders}) RETURNING id', values):
                    secure_token = await create_token(user)
                    if secure_token:
                        return JSONResponse(status_code=200, content={
                            "message": "Signed up successfully",
                            "user_token": secure_token
                        })
            except Exception as e:
                print_exception(signup.__name__, e)
                return JSONResponse(status_code=500, content={"message": "Something went wrong"})


@auth.post('/login')
async def login(user: LoginObject):
    async with get_connection() as conn:
        async with conn.cursor() as cur:
            try:
                if not await check_if_user_exists(cur, user.email):
                    return JSONResponse(status_code=409, content={"message": "Invalid credentials"})

                # TODO: Enforce encryption checking
                stored_password = await cur.fetch('SELECT password FROM users WHERE email = $1', user.email)
                if user.password == stored_password:
                    return JSONResponse(status_code=200, content={"message": "Logged in successfully"})
                return JSONResponse(status_code=409, content={"message": "Invalid credentials"})
            except Exception as e:
                print(f"login: {type(e)} - {str(e)}")
                return JSONResponse(status_code=500, content={"message": "Something went wrong", "error": str(e)})
