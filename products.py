import stripe

# Directory Module
from models import CreateProductObject

# FastAPI
from fastapi import APIRouter
from fastapi.responses import JSONResponse

products = APIRouter(prefix="/products", tags=['products'])


@products.post("/create")
async def create_product(product_request: CreateProductObject):
    try:
        product_request.stripe_account = "acct_1Q35XsQ8ogKFGPdO"

        product = await stripe.Product.create_async(
            **product_request.dict(exclude={'csrfmiddlewaretoken', 'unit_amount', 'currency'}),
        )

        price = await stripe.Price.create_async(
            product=product['id'],
            unit_amount=product_request.unit_amount,
            currency=product_request.currency,
            stripe_account=product_request.stripe_account
        )

        return JSONResponse(
            status_code=200, content={"product": {
                "id": product['id'],
                "price": price['unit_amount'],
                "name": product["name"],
                "description": product.get("description", None)
            }}
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "error": str(e),
            "type": f"{type(e)}"
        })
