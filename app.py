from contextlib import asynccontextmanager

from auth import auth
from payments import payments
from config import STRIPE_API_KEY
from db_connection import get_connection, init_db_pool, close_db_pool

# FastAPI
import uvicorn
from pydantic import ValidationError
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


class CustomHTTPException(HTTPException):
    def __init__(self, detail: str, status_code: int = 422):
        super().__init__(status_code=status_code, detail=detail)


# Env Vars
origins = [
    "http://127.0.0.1:8000"
]

# Initialisation
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db_pool()
    yield
    await close_db_pool()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_credentials=True
)

app.include_router(auth)
app.include_router(payments)


@app.get("/")
async def read_root():
    return {"status": 200, "message": "Success"}


if __name__ == "__main__":
    uvicorn.run("app:app", port=5000, reload=True)
