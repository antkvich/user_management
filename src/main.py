import logging.config

from fastapi import FastAPI

from src.auth.router import router as auth_router
from src.user.router import router as user_router

logging.config.fileConfig('logging.conf')


app = FastAPI()

app.include_router(
    user_router,
    tags=["User"],
    prefix="/user"
)
app.include_router(
    auth_router,
    tags=["Auth"],
    prefix="/auth"
)


@app.get("/")
async def root():
    return {"works": "yes"}

