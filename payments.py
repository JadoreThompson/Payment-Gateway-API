import sys

import stripe
from datetime import datetime

# Directory
from models import InvoiceObject

# FastAPI
from fastapi import APIRouter
from fastapi.responses import JSONResponse


payments = APIRouter(prefix='/payments', tags=['payments'])


# TODO: Make all forwarded to the connected account
def create_invoice_with_product_and_customer(og_data, days_until_due=None):
    """
    :param og_data: [dict] - contains the data for creating an invoice
    :param days_until_due: [int] - number of days until the invoice is due
    :return: InvoiceItem object
    """
    data = {k: v for k, v in og_data.items() if v is not None}
    connect_account_id = data.get("issuer", {}).get("account")

    try:
        product = stripe.Product.create(
            name=data.get("new_product", {}).get("name"),
            active=data.get("new_product", {}).get("active"),
            stripe_account=connect_account_id
        )

        price = stripe.Price.create(
            product=product['id'],
            unit_amount=data.get('unit_amount'),
            currency=data.get('currency'),
            stripe_account=connect_account_id
        )

        customer = stripe.Customer.create(
            name=data.get("new_customer", {}).get("name"),
            email=data.get("new_customer", {}).get("email"),
            description=data.get("new_customer", {}).get("description", None),
            stripe_account=connect_account_id
        )

        invoice = stripe.Invoice.create(
            customer=customer['id'],
            collection_method='send_invoice',
            stripe_account=connect_account_id,
            application_fee_amount=int(data.get("unit_amount", 0) * 0.02),
            days_until_due=days_until_due,
            # issuer={
            #     "type": data.get("issuer", {}).get("type"),
            #     "account": connect_account_id
            # },
            # transfer_data={
            #     'destination': connect_account_id
            # }
        )
        return stripe.InvoiceItem.create(customer=customer['id'], price=price['id'], invoice=invoice['id'], stripe_account=connect_account_id)
    
    except Exception as e:
        raise Exception(f"Line {sys.exc_info()[-1].tb_lineno}| [{create_invoice_with_product_and_customer.__name__}] - {e}")


def create_invoice_with_existing_customer(data):
    pass


@payments.post("/invoice/create")
async def create_invoice(invoice_request: InvoiceObject):
    """
    :param invoice_request:
    :return:
    -   200, Successfully created invoice
    -   500, Server Error
    """
    try:
        # Calculating the days until due
        invoice_request_due_date = datetime.strptime(invoice_request.due_date, "%m/%d/%Y")
        date = datetime.now()
        days_until_due = invoice_request_due_date - date

        # Creating the invoice
        invoice = create_invoice_with_product_and_customer(invoice_request.dict(), int(days_until_due.days))
        return JSONResponse(status_code=200, content={"message": "Successfully created invoice", 'extra': invoice})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"message": "Something went wrong", 'type': f"Type: {type(e)}", 'detail': str(e)})


@payments.put("/invoice/update")
async def update_invoice(update_invoice_request: str):
    pass


@payments.delete("/invoice/delete")
async def delete_invoice(delete_invoice_request: str):
    pass
