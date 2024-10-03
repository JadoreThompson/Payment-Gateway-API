import json
import sys
import stripe
import httpx
from datetime import datetime

# Directory
from models import InvoiceObject, InvoiceDeleteObject, UpdateInvoiceObject, StatRequestObject
from tools import deep_convert_to_dict
# FastAPI
from fastapi import APIRouter
from fastapi.responses import JSONResponse


# Init
payments = APIRouter(prefix='/payments', tags=['payments'])


async def create_invoice_with_new_product_and_customer(og_data, days_until_due=None):
    """
    :param og_data: [dict] - contains the data for creating an invoice
    :param days_until_due: [int] - number of days until the invoice is due
    :return: InvoiceItem object
    """
    data = dict({k: v for k, v in og_data.items() if v is not None})
    data = deep_convert_to_dict(data)
    connect_account_id = data.get("issuer", {}).get("account")


    try:
        product = await stripe.Product.create_async(
            name=data.get("new_product", {}).get("name"),
            description=data.get("new_product", {}).get("description"),
            active=data.get("new_product", {}).get("active"),
            stripe_account=connect_account_id
        )

        price = await stripe.Price.create_async(
            product=product['id'],
            unit_amount=data.get('unit_amount'),
            currency=data.get('currency'),
            stripe_account=connect_account_id
        )

        customer = await stripe.Customer.create_async(
            name=data.get("new_customer", {}).get("name"),
            email=data.get("new_customer", {}).get("email"),
            description=data.get("new_customer", {}).get("description", None),
            stripe_account=connect_account_id
        )

        invoice = await stripe.Invoice.create_async(
            auto_advance=True, #  data['auto_advance'],
            customer=customer['id'],
            collection_method='send_invoice',
            stripe_account=connect_account_id,
            application_fee_amount=int(data.get("unit_amount", 0) * 0.02),
            days_until_due=days_until_due,
        )
        return await stripe.InvoiceItem.create_async(customer=customer['id'], price=price['id'], invoice=invoice['id'], stripe_account=connect_account_id)
    
    except Exception as e:
        print(f"Line {sys.exc_info()[-1].tb_lineno}| [{create_invoice_with_new_product_and_customer.__name__}] - {e}")
        raise Exception(f"Line {sys.exc_info()[-1].tb_lineno}| [{create_invoice_with_new_product_and_customer.__name__}] - {e}")


async def create_invoice_with_existing_customer(og_data, days_until_due):
    """
    Creates an invoice for an existing customer using provided data.

    :param og_data: [dict] - contains the data for creating an invoice
    :param days_until_due: [int] - number of days until the invoice is due
    :return: InvoiceItem object
    """
    data = {k: v for k, v in og_data.items() if v is not None}
    connect_account_id = data.get("issuer", {}).get("account")

    try:
        product = await stripe.Product.create_async(
            name=data.get("new_product", {}).get("name"),
            active=data.get("new_product", {}).get("active"),
            stripe_account=connect_account_id
        )

        price = await stripe.Price.create_async(
            product=product['id'],
            unit_amount=data.get('unit_amount'),
            currency=data.get('currency'),
            stripe_account=connect_account_id
        )

        invoice = await stripe.Invoice.create_async(
            auto_advance=data.get('auto_advance', True),
            customer=data.get("customer_id"),
            collection_method='send_invoice',
            stripe_account=connect_account_id,
            application_fee_amount=int(data.get("unit_amount", 0) * 0.02),
            days_until_due=days_until_due,
        )
        return await stripe.InvoiceItem.create_async(customer=data.get('customer_id'), price=price['id'], invoice=invoice['id'],
                                     stripe_account=connect_account_id)
    except Exception as e:
        raise Exception(f"Line {sys.exc_info()[-1].tb_lineno}| [{create_invoice_with_existing_customer.__name__}] - {e}")


async def create_invoice_with_product_id(og_data, days_until_due):
    """
    Creates a draft invoice using a product ID and a new customer.

    :param og_data: [dict] - contains the data for creating an invoice
    :param days_until_due: [int] - number of days until the invoice is due
    :return: InvoiceItem object
    """
    data = {k: v for k, v in og_data.items() if v is not None}
    connect_account_id = data.get("issuer", {}).get("account")

    try:
        price = await stripe.Price.list_async(
            product=data["product_id"],
            stripe_account=connect_account_id
        ).get('data', [])[0].get('id')

        customer = await stripe.Customer.create_async(
            name=data.get("new_customer", {}).get("name"),
            email=data.get("new_customer", {}).get("email"),
            description=data.get("new_customer", {}).get("description", None),
            stripe_account=connect_account_id
        )

        invoice = await stripe.Invoice.create_async(
            customer=customer['id'],
            collection_method='send_invoice',
            stripe_account=connect_account_id,
            application_fee_amount=int(data.get("unit_amount", 0) * 0.02),
            days_until_due=days_until_due,
        )
        return await stripe.InvoiceItem.create_async(customer=customer['id'], price=price, invoice=invoice['id'],
                                         stripe_account=connect_account_id)
    except Exception as e:
        raise Exception(f"Line {sys.exc_info()[-1].tb_lineno}| [{create_invoice_with_product_id.__name__}] - {e}")


async def create_invoice_with_premade_entities(og_data, days_until_due):
    """
    Creates a draft invoice using premade entities for a specified customer.

    :param og_data: [dict] - contains the data for creating an invoice
    :param days_until_due: [int] - number of days until the invoice is due
    :return: InvoiceItem object
    """
    data = {k: v for k, v in og_data.items() if v is not None}
    connect_account_id = data.get("issuer", {}).get("account")

    try:
        price = await stripe.Price.list_async(
            product="prod_Qv6PIuYELoWeK6",
            stripe_account="acct_1Q35XsQ8ogKFGPdO"
        ).get('data', [])[0].get('id')

        invoice = await stripe.Invoice.create_async(
            customer=data['customer_id'],
            collection_method='send_invoice',
            stripe_account=connect_account_id,
            application_fee_amount=int(data.get("unit_amount", 0) * 0.02),
            days_until_due=days_until_due
        )
        return await stripe.InvoiceItem.create_async(customer=data['customer_id'], price=price, invoice=invoice['id'],
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
        invoice_request_due_date = datetime.strptime(invoice_request.due_date, "%Y-%m-%d")
        date = datetime.now()
        until_due = (invoice_request_due_date - date).days
        days_until_due = int(until_due)

        invoice_request_obj = invoice_request.__dict__
        invoice_request_obj['issuer'] = {'type': 'account'}
        # invoice_request_obj['issuer']['account'] = 'acct_1Q35XsQ8ogKFGPdO'
        invoice_request_obj['issuer']['account'] = invoice_request.stripe_account

        async with httpx.AsyncClient() as client:
            # Creating the invoice
            if invoice_request.customer_id and not invoice_request.product_id:
                invoice = await create_invoice_with_existing_customer(invoice_request.__dict__, days_until_due)
            elif invoice_request.product_id and not invoice_request.customer_id:
                invoice = await create_invoice_with_product_id(invoice_request.__dict__, days_until_due)
            elif invoice_request.product_id and invoice_request.customer_id:
                invoice = await create_invoice_with_premade_entities(invoice_request.__dict__, days_until_due)
            else:
                invoice = await create_invoice_with_new_product_and_customer(og_data=invoice_request.__dict__, days_until_due=days_until_due)

            status = 'draft'
            # Finalising
            if invoice_request.draft == False:
                print("Finalizing invoice")
                await stripe.Invoice.finalize_invoice_async(invoice.invoice, stripe_account=invoice_request.stripe_account)
                status = 'open'

        return JSONResponse(status_code=200, content={
            "message": "Successfully created invoice",
            'invoice': {
                "invoice": invoice['invoice'],
                "amount": invoice['amount'],
            },
            "status": status
        })
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"message": "Something went wrong", 'type': f"Type: {type(e)}", 'detail': str(e)})


@payments.put("/invoice/update")
async def update_invoice(update_invoice_request: UpdateInvoiceObject):
    try:
        keys_to_drop = [
            "amount_shipping", "amount_paid", "billing_reason", "customer_email", "period_start",
            "object", "post_payment_credit_notes_amount", "status", "customer_tax_exempt", "period_end",
            "attempted", "amount_remaining", "subtotal_excluding_tax", "subtotal", "currency",
            "customer", "total_excluding_tax", "created", "amount_due", "pre_payment_credit_notes_amount",
            "livemode", "attempt_count", "total", "webhooks_delivered_at", "account_country",
            "customer_name", "lines", "paid_out_of_band", "account_name", "starting_balance", "application",
            'paid'
        ]
        current_invoice_item = await stripe.InvoiceItem.list_async(
            invoice=update_invoice_request.id,
            stripe_account=update_invoice_request.stripe_account
        )
        current_invoice_item = dict(current_invoice_item['data'][0])

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Something went wrong", 'type': f"Type: {type(e)}", 'detail': str(e)})



@payments.delete("/invoice/delete")
async def delete_invoice(delete_invoice_request: InvoiceDeleteObject):
    try:
        # Can only delete draft invoices
        stripe.Invoice.delete(delete_invoice_request.invoice_id, stripe_account=delete_invoice_request.connected_account_id)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"message": "Something went wrong"})



@payments.post("/get-stats")
async def get_stats(stats_request: StatRequestObject):
    try:
        today_midnight = int(datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0).timestamp())
        yesterday_midnight = today_midnight - 86400

        func_args = {**stats_request.dict(), "created": {}}
        balance = await stripe.Balance.retrieve_async(**stats_request.dict())
        balance = balance['available'][0]['amount']

        # Sales
        func_args['created']['gt'] = today_midnight
        todays_data = await stripe.PaymentIntent.list_async(**func_args)
        todays_sales = sum(item['amount_received'] for item in todays_data['data']) / 100
        try: todays_average_order_value = todays_sales / len(todays_data['data'])
        except ZeroDivisionError: todays_average_order_value = 0

        func_args["created"]["gt"] = yesterday_midnight
        func_args['created']['lt'] = today_midnight
        yesterday_data = await stripe.PaymentIntent.list_async(**func_args)
        yesterday_sales = sum(item['amount_received'] for item in todays_data['data'])
        try: yesterday_average_order_value = todays_sales / len(yesterday_data['data'])
        except ZeroDivisionError: yesterday_average_order_value = 0

        avg_order_value_growth = todays_average_order_value - yesterday_average_order_value

        try:
            sales_growth = todays_sales - yesterday_sales / yesterday_sales * 100
        except ZeroDivisionError:
            sales_growth = 0

        # Customers
        yesterday_customers = await stripe.Customer.list_async(**func_args)
        yesterday_customers_count = len(yesterday_customers['data'])

        del func_args['created']['lt']
        func_args['created']['gt'] = today_midnight
        today_customers = await stripe.Customer.list_async(**func_args)
        today_customers_count = len(today_customers['data'])
        customer_growth = today_customers_count - yesterday_customers_count

        # Transactions
        try:
            todays_transactions = await stripe.issuing.Transaction.list(**func_args)
            transaction_count = len(todays_transactions['data'])
        except Exception as e:
            print(f"{type(e)} - {str(e)}")
            transaction_count = 0

        content = {
            "balance": balance,
            "todays_sales": todays_sales,
            "sales_growth": sales_growth,
            "todays_customers": today_customers_count,
            "customer_growth": customer_growth,
            "transaction_count": transaction_count,
            "todays_avg_order_value": todays_average_order_value,
            "avg_order_value_growth": avg_order_value_growth
        }
        return JSONResponse(status_code=200, content=content)
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"message": "Something went wrong", 'type': f"Type: {type(e)}", 'detail': str(e)})
