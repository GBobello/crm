import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import auth, lawyer, customer, position
from app.db.init_db import init_db
from app.core.config import settings

load_dotenv()

app = FastAPI(redoc_url=None, docs_url=None)

if settings.debug:
    app = FastAPI()


@app.on_event("startup")
def startup():
    init_db()


app.mount(
    "/static", StaticFiles(directory=os.path.join("app", "static")), name="static"
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(lawyer.router, prefix="/lawyers", tags=["lawyers"])
app.include_router(customer.router, prefix="/customers", tags=["customers"])
app.include_router(position.router, prefix="/positions", tags=["positions"])
