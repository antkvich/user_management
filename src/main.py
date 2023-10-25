from fastapi import FastAPI
import logging.config
from src.config import settings


logging.config.fileConfig('logging.conf')


app = FastAPI()


@app.get("/")
async def root():
    return {"works": "yes"}


