from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import engine
from models import Base

from routers.ingest import router


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)


app.include_router(router)


# Serve frontend
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")


@app.get("/")
def home():
    return {
        "message": "Generic Data Ingestion Service"
    }