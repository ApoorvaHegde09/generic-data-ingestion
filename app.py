from fastapi import FastAPI

from database import engine
from models import Base

from routers.ingest import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Generic Data Ingestion Service"
    }