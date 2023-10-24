from fastapi import FastAPI
from database import get_session

app = FastAPI()


@app.get("/")
async def root():
    return {"works": "yes"}


