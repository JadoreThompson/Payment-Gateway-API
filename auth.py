from db_connection import get_connection
# from models import
from tools import print_exception

import stripe

# FastAPI
from fastapi import APIRouter
from fastapi.responses import JSONResponse


# Initialisation
auth = APIRouter(prefix="/auth", tags=["auth"])


# Important
''' Defaults
"requirement_collection": "application",
"fees": {"payer": "application"},
"losses": {"payments": "application"},
"stripe_dashboard": {"type": "none"}


'''

''' Variables

'''


@auth.post("/create-account")
async def create_account(token):
    account = stripe.Account.create(
        country="GB",
        email="johnemal@gmail.com",
        controller={
            "requirement_collection": "application",
            "fees": {"payer": "application"},
            "losses": {"payments": "application"},
            "stripe_dashboard": {"type": "none"}
        },
        account_token=token
    )
    return account


@auth.post("/create-token")
async def create_token():
    try:
        token = stripe.Token.create(
            account={
                "business_type": "individual",
                "individual": {"first_name": "Jack", "last_name": "Days"},
                "tos_shown_and_accepted": True,
            },
        )
        print(type(token))
        item = await create_account(token=token)
        return item
    except Exception as e:
        print_exception(create_token.__name__, e)
        return False
