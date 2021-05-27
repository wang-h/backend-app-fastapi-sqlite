
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from .routers import tasks
from .routers import knowledgebases
from .routers import users
from .routers import admin

origins = [
    "http://127.0.0.1:8080"

]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(
    tasks.router,
    prefix="/api/task",
    tags=["task"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    knowledgebases.router,
    prefix="/api/kb",
    tags=["kb"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    users.router,
    prefix="/api/user",
    tags=["user"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    admin.router,
    prefix="/api/admin",
    tags=["admin"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@app.get("/api/task")
async def root():
    return {"message": "Hello Bigger Applications!"}
