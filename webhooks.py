import asyncio
import aiohttp
import json

import stripe

# Dir
from models import CreateProductObject

# FastAPI
from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import JSONResponse


webhooks = APIRouter(prefix='/webhooks', tags=['webhooks'])

DJANGO_URL = 'http://127.0.0.1:8000/api'


@webhooks.get('/')
async def read_root():
    return {"message": "Running"}


@webhooks.post('/invoice/receive')
async def webhook_invoice(request: Request, bg_task: BackgroundTasks):
    body = await request.body()
    bg_task.add_task(process_bytes, body, 1)
    return JSONResponse(status_code=202, content={"message": "Successfully received event"})


async def process_bytes(body: bytes, path: int = None):
    try:
        event = json.loads(body)
        if path == 1:
            await process_invoice_event(event)
        if path == 0:
            await process_transaction_event(event)
    except Exception as e:
        print(f"({process_bytes.__name__}) {type(e)} - {str(e)}")


async def process_invoice_event(event: dict):
    try:
        if event['type'] == 'invoice.paid':
            content = {
                'type': 'invoice.paid',
                'data': {
                    'invoice_id': event['data']['object']['id'],
                    'amount_paid': event['data']['object']['amount_paid'],
                    'created': event['data']['object']['created']
                }
            }
            async with aiohttp.ClientSession() as session:
                await session.post(f"{DJANGO_URL}/receive-invoice-updates", json=content)

        if event['type'] == 'invoice.deleted':
            content = {
                'type': 'invoice.deleted',
                'data': {
                    'invoice_id': event['data']['object']['id'],
                    'created': event['data']['object']['created']
                }
            }
            async with aiohttp.ClientSession() as session:
                await session.post(f"{DJANGO_URL}/receive-invoice-updates", json=content)
    except Exception as e:
        print(type(e), str(e))


@webhooks.post("/transactions/receive")
async def webhook_transaction(request: Request, bg_task: BackgroundTasks):
    body = await request.body()
    bg_task.add_task(process_bytes, body, 0)
    return JSONResponse(status_code=202, content={"message": "Successfully received event"})


async def process_transaction_event(event: dict):
    try:
        if event['type'] == 'charge.succeeded':
            content = {
                'type': 'charge.succeeded',
                'data': {
                    'transaction_id': event['data']['object']['id'],
                    'amount': event['data']['object']['amount_captured'],
                    'created': event['data']['object']['created']
                }
            }
            print(json.dumps(event, indent=4))
            async with aiohttp.ClientSession() as session:
                await session.post(f"{DJANGO_URL}/receive-transaction-updates", json=content)
    except Exception as e:
        print(type(e), str(e))


print(json.dumps(stripe.Charge.retrieve("ch_3Q5Q80L8QfTmAOru1jPqwJDJ"), indent=4))
#print(json.dumps(stripe.Invoice.retrieve("in_1Q5Q7zL8QfTmAOruzYCSPdOc"), indent=4))
