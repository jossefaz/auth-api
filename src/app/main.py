from fastapi import FastAPI
from .api import monitor, token

app = FastAPI()

app.include_router(monitor.router, prefix="/monitor", tags=["monitoring"])
app.include_router(token.router, prefix="/auth", tags=["Oauth"])

