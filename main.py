import os
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from user_router import router as user_router
from profile_router import router as profile_router
from db import create_tables, delete_tables
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("База готова")
    yield
    await delete_tables()
    print("База очищена")


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(profile_router)


@app.get("/")
async def main() -> JSONResponse:
    return JSONResponse(status_code=200, content="Manager-App")


if __name__ == "__main__":
    server_address = os.getenv('SERVER_ADDRESS')
    host, port = server_address.split(":")
    uvicorn.run(app, host=host, port=int(port))
