import datetime
import json
from typing import Optional, Annotated

import stripe

# FastAPI
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from stripe import InvalidRequestError

# Directory Modules
from Resources.validators import check_if_user_exists, validate_password
from db_connection import get_connection
from models import (
    LoginObject,
    StripeSignUpObject,
    AccountUpdateBusinessProfileObject
)

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
        return JSONResponse(status_code=200, content={
            "message": "Successfully created user", 'account': {'account': account['id']}
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Internal server error", "type": f"{type(e)}", "detail": str(e)})


@auth.post("/update-user")
async def update_user(update_bank_info: Annotated[str, Form(...)] = None, update_individual_request: Annotated[str, Form(...)] = None, individual_file: Annotated[bytes | UploadFile, File()] = None, update_business_profile_request: Optional[AccountUpdateBusinessProfileObject] = None):
    try:
        if update_business_profile_request is not None:
            # Sending docs off to stripe
            await stripe.Account.modify_async(
                stripe_account=update_business_profile_request.stripe_account,
                business_profile={'url': update_business_profile_request.url, 'mcc': update_business_profile_request.industry},
            )

        if update_individual_request is not None:
            # Reading and downloading the file, before sending off to stripe
            fbytes = await individual_file.read()
            file_path = "temp/{}".format(individual_file.filename)

            with open(file_path, "wb") as temp_file:
                temp_file.write(fbytes)
            with open(file_path, 'rb') as fp:
                file_token = await stripe.File.create_async(file=fp, purpose='account_requirement')

            individual_request_data = json.loads(update_individual_request)

            individual_request_data['verification'] = {'document': {'front': file_token['id']}}
            token = await stripe.Token.create_async(account={"individual": individual_request_data['individual']})
            await stripe.Account.modify_async(account_token=token, stripe_account=individual_request_data['stripe_account'],)

        if update_bank_info is not None:
            bank_dict = json.loads(update_bank_info)
            stripe_account = bank_dict['stripe_account']

            del bank_dict['stripe_account']
            bank_token = await stripe.Token.create_async(bank_account=bank_dict)

            await stripe.Account.modify_async(stripe_account=stripe_account, external_account=bank_token['id'])

        return JSONResponse(status_code=200, content={"message": 'Successfully updated account', 'time': datetime.datetime.now().timestamp()})
    except InvalidRequestError as e:
        return JSONResponse(status_code=500, content={"message": "Error", 'error': f"{str(e).split(":")[1]}"})
    except Exception as e:
        print(f"{type(e)} - {str(e)}")
        return JSONResponse(status_code=500, content={"message": "Error", "error": f"{str(e)}"})
