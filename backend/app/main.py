import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import auth, lawyer
from app.db.init_db import init_db
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@app.on_event("startup")
def startup():
    init_db()


app.mount(
    "/static", StaticFiles(directory=os.path.join("app", "static")), name="static"
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(lawyer.router, prefix="/lawyers", tags=["lawyers"])
