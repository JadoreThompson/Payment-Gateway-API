import stripe

# Directory Modules
from models import CustomerObject

# FastAPI Modules
from fastapi import APIRouter
from fastapi.responses import JSONResponse

customer = APIRouter(prefix='/customer', tags=['customer'])


@customer.post('/create')
async def create_customer(customer_request: CustomerObject):
        try:
            customer = await stripe.Customer.create_async(**customer_request.dict(exclude={'stripe_account'}), stripe_account="acct_1Q35XsQ8ogKFGPdO")
            return JSONResponse(
                status_code=200, content={"customer": customer}
            )
        except Exception as e:
            return JSONResponse(
                status_code=500, content={"error": str(e), "type": f"{type(e)}"}
            )
