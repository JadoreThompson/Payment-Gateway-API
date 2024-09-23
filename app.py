from contextlib import asynccontextmanager

from auth import auth
from config import STRIPE_API_KEY
from db_connection import get_connection, init_db_pool, close_db_pool

# FastAPI
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Env Vars
origins = [
    "http://127.0.0.1:5000/auth/signup"
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


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return {"caught"}


@app.get("/")
async def read_root():
    return {"status": 200, "message": "Success"}


if __name__ == "__main__":
    uvicorn.run("app:app", port=5000, reload=True)
