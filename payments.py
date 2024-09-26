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
def create_invoice_with_new_product_and_customer(og_data, days_until_due=None):
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
        )
        return stripe.InvoiceItem.create(customer=customer['id'], price=price['id'], invoice=invoice['id'], stripe_account=connect_account_id)
    
    except Exception as e:
        raise Exception(f"Line {sys.exc_info()[-1].tb_lineno}| [{create_invoice_with_new_product_and_customer.__name__}] - {e}")


def create_invoice_with_existing_customer(og_data, days_until_due):
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

        invoice = stripe.Invoice.create(
            customer=data.get("customer_id"),
            collection_method='send_invoice',
            stripe_account=connect_account_id,
            application_fee_amount=int(data.get("unit_amount", 0) * 0.02),
            days_until_due=days_until_due,
        )
        return stripe.InvoiceItem.create(customer=data.get('customer_id'), price=price['id'], invoice=invoice['id'],
                                     stripe_account=connect_account_id)
    except Exception as e:
        raise Exception(f"Line {sys.exc_info()[-1].tb_lineno}| [{create_invoice_with_existing_customer.__name__}] - {e}")


def create_invoice_with_product_id(og_data, days_until_due):
    data = {k: v for k, v in og_data.items() if v is not None}
    connect_account_id = data.get("issuer", {}).get("account")

    try:
        price = stripe.Price.list(
            product=data["product_id"],
            stripe_account=connect_account_id
        ).get('data', [])[0].get('id')

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
        )
        return stripe.InvoiceItem.create(customer=customer['id'], price=price, invoice=invoice['id'],
                                         stripe_account=connect_account_id)
    except Exception as e:
        raise Exception(f"Line {sys.exc_info()[-1].tb_lineno}| [{create_invoice_with_product_id.__name__}] - {e}")

    pass


def create_invoice_with_premade_entities(og_data, days_until_due):
    data = {k: v for k, v in og_data.items() if v is not None}
    connect_account_id = data.get("issuer", {}).get("account")

    try:
        price = stripe.Price.list(
            product="prod_Qv6PIuYELoWeK6",
            stripe_account="acct_1Q35XsQ8ogKFGPdO"
        ).get('data', [])[0].get('id')

        invoice = stripe.Invoice.create(
            customer=data['customer_id'],
            collection_method='send_invoice',
            stripe_account=connect_account_id,
            application_fee_amount=int(data.get("unit_amount", 0) * 0.02),
            days_until_due=days_until_due
        )
        return stripe.InvoiceItem.create(customer=data['customer_id'], price=price, invoice=invoice['id'],
                                         stripe_account=connect_account_id)
    except Exception as e:
        raise Exception(f"Line {sys.exc_info()[-1].tb_lineno}| [{create_invoice_with_premade_entities.__name__}] - {e}")



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
        if invoice_request.customer_id and not invoice_request.product_id:
            invoice = create_invoice_with_existing_customer(invoice_request.dict(), int(days_until_due.days))
        elif invoice_request.product_id and not invoice_request.customer_id:
            invoice = create_invoice_with_product_id(invoice_request.dict(), int(days_until_due.days))
        elif invoice_request.product_id and invoice_request.customer_id:
            invoice = create_invoice_with_premade_entities(invoice_request.dict(), int(days_until_due.days))
        else:
            invoice = create_invoice_with_new_product_and_customer(invoice_request.dict(), int(days_until_due.days))

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


#  print(stripe.Price.list(product='prod_Qv5GaUG0ZPrtOY', stripe_account='acct_1Q35XsQ8ogKFGPdO')['data'][0]['id'])
