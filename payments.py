import stripe
from datetime import datetime

# Directory
from models import InvoiceObject

# FastAPI
from fastapi import APIRouter
from fastapi.responses import JSONResponse


payments = APIRouter(prefix='/payments', tags=['payments'])


def create_invoice_with_product_and_customer(data, days_until_due):
    """
    :param days_until_due:
    :param data: [dict]
    :return: InvoiceItem
    """
    data = {k: v for k, v in data if data[k] is not None}

    # product = stripe.Product.create(name=data["product"]["name"],active=data["product"]["active"])
    # price = stripe.Price.create(product=product['id'], unit_amount=data['unit_amount'], currency=data['currency'])
    # customer = stripe.Customer.create(
    #     name=data["customer"]["name"],email=data["customer"]["email"],description=data["customer"]["description"])
    # invoice = stripe.Invoice.create(customer=customer['id'], collection_method='send_invoice', stripe_account=data["connect_account"],
    #                                 application_fee_amount=data["unit_amount"] * 0.02, days_until_due=days_until_due)
    #
    # return stripe.InvoiceItem.create(customer=customer['id'], price=price['id'], invoice=invoice['id'])

    product = stripe.Product.create(name=data.get("product", {}).get("name", None),
                                    active=data.get("product", {}).get("active", None))
    price = stripe.Price.create(product=product['id'], unit_amount=data.get('unit_amount', None),
                                currency=data.get('currency', None))
    customer = stripe.Customer.create(name=data.get("customer", {}).get("name", None),
                                      email=data.get("customer", {}).get("email", None),
                                      description=data.get("customer", {}).get("description", None))
    invoice = stripe.Invoice.create(customer=customer['id'], collection_method='send_invoice',
                                    stripe_account=data.get("connect_account", None),
                                    application_fee_amount=data.get("unit_amount", 0) * 0.02,
                                    days_until_due=days_until_due)
    return stripe.InvoiceItem.create(customer=customer['id'], price=price['id'], invoice=invoice['id'])


def create_invoice_with_existing_customer(data):


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
        create_invoice_with_product_and_customer(invoice_request.dict(), int(days_until_due.days))
        return JSONResponse(status_code=200, content={"message": "Successfully created invoice"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Something went wrong", 'detail': str(e)})


@payments.put("/invoice/update")
async def update_invoice(update_invoice_request: str):
    pass


@payments.delete("/invoice/delete")
async def delete_invoice(delete_invoice_request: str):
    pass
