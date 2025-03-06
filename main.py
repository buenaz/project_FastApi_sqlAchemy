import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from users.user_router import router as user_router
from profiles.profile_router import router as profile_router
from projects.project_router import router as project_router
from tasks.task_router import router as task_router
from db import create_tables, delete_tables

app = FastAPI()

app.include_router(user_router)
app.include_router(profile_router)
app.include_router(project_router)
app.include_router(task_router)


@app.get("/")
async def main() -> JSONResponse:
    return JSONResponse(status_code=200, content="Manager-App")


@app.get("start")
async def start() -> JSONResponse:
    await create_tables()
    return JSONResponse(status_code=200, content="Базы данных созданы")


@app.get("finish")
async def finish() -> JSONResponse:
    await delete_tables()
    return JSONResponse(status_code=200, content="Таблицы очищены")


if __name__ == "__main__":
    server_address = os.getenv('SERVER_ADDRESS')
    host, port = server_address.split(":")
    uvicorn.run(app, host=host, port=int(port))
