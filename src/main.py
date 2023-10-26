from fastapi import FastAPI
import logging.config
from src.config import settings
from src.database import get_session


logging.config.fileConfig('logging.conf')


app = FastAPI()


@app.get("/")
async def root():
    return {"works": "yes"}

