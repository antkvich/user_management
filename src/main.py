from fastapi import FastAPI
import logging.config
from src.config import Settings

settings = Settings()

logging.config.fileConfig('logging.conf')

app = FastAPI()


@app.get("/")
async def root():
    return {"works": "yes"}


