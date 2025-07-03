from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import ops, client
from app.database import Base, engine
import os

app = FastAPI(title="Secure File Sharing System")


@app.on_event("startup")
def on_startup():
    if not os.path.exists("files"):
        os.makedirs("files")
    Base.metadata.create_all(bind=engine)

app.include_router(ops.router)
app.include_router(client.router) 