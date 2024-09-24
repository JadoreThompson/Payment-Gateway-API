import re
from contextlib import asynccontextmanager
from typing import Tuple

from Resources.validators import check_if_user_exists, validate_password
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
async def signup(user: SignUpObject):
    try:
        validate_password(user.password)
    except ValueError as e:
        return JSONResponse(status_code=409, content={"message": str(e)})
    return JSONResponse(status_code=200, content={"message": "Successfully signed up", "user": user.dict()})


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
