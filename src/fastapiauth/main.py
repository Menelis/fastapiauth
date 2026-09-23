import os

from fastapi import FastAPI
from .routers.auth_routes import auth_router

app = FastAPI(debug=os.getenv("DEBUG", "False"))
app.include_router(auth_router)