from auth import auth
from config import STRIPE_API_KEY

# FastAPI
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


app = FastAPI()
app.include_router(auth)


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return {"caught"}


@app.get("/")
async def read_root():
    return {"status": 200, "message": "Success"}


if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, reload=True)
