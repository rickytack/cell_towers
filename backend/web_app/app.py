import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import exists, select

from api.v1.api import router as api_router
from db.session import AsyncSessionLocal
from models.models import CellTower


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    # Run on startup
    print("Starting FastAPI app", flush=True)
    async with AsyncSessionLocal() as session:
        is_empty = not (await session.scalar(select(exists().select_from(CellTower))))
        if is_empty:
            print("CellTower is empty. Prefilling it")
            await CellTower.import_opencellid_towers("/app/misc/250.csv")
        else:
            print("CellTower is not empty")

    yield

app = FastAPI(lifespan=lifespan, debug=True)

@app.middleware("http")
async def log_cors_requests(request: Request, call_next):
    origin = request.headers.get("origin")
    if origin:
        print(f"⚠️ Incoming request from origin: {origin}")
    response = await call_next(request)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1"],
    allow_methods=["GET"],
)

app.include_router(api_router, prefix="/api")

#