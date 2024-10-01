import asyncio
import json

# Dir
from models import CreateProductObject

# FastAPI
from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import JSONResponse


webhook = APIRouter(prefix='/webhooks', tags=['webhooks'])


@webhook.get('/')
async def read_root():
    return {"message": "Running"}


@webhook.post('/invoice/receive')
async def webhook_invoice(request: Request, bg_task: BackgroundTasks):
    body = await request.body()
    bg_task.add_task(process_bytes, body)
    return JSONResponse(status_code=200, content={"message": "Successfully received event"})


async def process_bytes(body: bytes):
    try:
        event = json.loads(body)
        await process_event(event)
    except Exception as e:
        print(f"({process_bytes.__name__}) {type(e)} - {str(e)}")


async def process_event(event: dict):
    if event['type'] == 'invoice.paid':
        content = {
            'type': 'invoice.paid',
            'data': {
                'invoice_id': event['data']['object']['id'],
                'amount_paid': event['data']['object']['amount_paid'],
                'created': event['data']['object']['created']
            }
        }
        print(json.dumps(content, indent=4))
        return JSONResponse(status_code=200, content=content)

    if event['type'] == 'invoice.deleted':
        content = {
            'type': 'invoice.deleted',
            'data': {
                'invoice_id': event['data']['object']['id'],
                'created': event['data']['object']['created']
            }
        }
        print(json.dumps(content, indent=4))
        return JSONResponse(status_code=200, content=content)


@webhook.get("/transactions/receive")
async def webhook_transaction(request: Request):
    json_data = await request.json()
