from fastapi import FastAPI
import logging.config
from src.user.router import router as user_router
from src.auth.router import router as auth_router

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

