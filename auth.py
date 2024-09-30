import datetime
import time
import stripe
import re
from contextlib import asynccontextmanager
from typing import Tuple
import asyncpg

# Directory Modules
from Resources.validators import check_if_user_exists, validate_password
from db_connection import get_connection
from models import (
    LoginObject,
    StripeSignUpObject,
    SignUpObject,
    TokenCreateObject,
    CreateAccountObject,
    AccountToken, UpdateAccountObject
)
from tools import print_exception, get_cols_and_placeholders

# FastAPI
from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse


# Initialisation
auth = APIRouter(prefix="/auth", tags=["auth"])


def create_token(business_type: str, fname: str, lname: str, tos: bool):
    """
    :param business_type:
    :param fname:
    :param lname:
    :param tos:
    :return: Token: stripe._token.Token
    """
    user_token = stripe.Token.create(
        account={
            "business_type": business_type,
            "individual": {"first_name": fname, "last_name": lname},
            "tos_shown_and_accepted": tos
        }
    )
    return user_token


def create_account(email: str, token):
    """
    :param email:
    :param token:
    :return: Token: stripe._account.Account
    """
    account = stripe.Account.create(
        email=email,
        controller={
            "fees": {"payer": "application"},
            "losses": {"payments": "application"},
            "stripe_dashboard": {"type": "none"},
            "requirement_collection": "application"
        },
        capabilities={
            "card_payments": {"requested": True},
            "transfers": {"requested": True}
        },
        account_token=token
    )
    return account


@auth.post('/signup')
async def signup(user: StripeSignUpObject):
    """
    :param user:
    :return:
    """

    # Note: Send email confirmation for security
    try:
        validate_password(user.password)
    except ValueError as e:
        return JSONResponse(status_code=409, content={"message": str(e)})

    try:
        token = create_token(user.business_type, user.first_name, user.last_name, user.tos_shown_and_accepted)
        account = create_account(user.email, token)
        return JSONResponse(status_code=200, content={"message": "Successfully created user", 'account': {'account': account['id']}})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Internal server error", "type": f"{type(e)}", "detail": str(e)})


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


from tools import deep_convert_to_dict
@auth.post("/update-user")
async def update_user(update_request: UpdateAccountObject):
    try:
        del update_request.type
        del update_request.controller
        data = deep_convert_to_dict(update_request.__dict__)
        token = await stripe.Token.create_async(account={"individual": data['individual']})
        await stripe.Account.modify_async(account_token=token, stripe_account=update_request.stripe_account)
    except Exception as e:
        print(f"{type(e)} - {str(e)}")
        return JSONResponse(status_code=500, content={"message": "Error", "error": str(e)})


from config import *
# stripe.Account.delete("acct_1Q2hFXPr8ejCg2qQ")
