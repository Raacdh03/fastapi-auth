from fastapi import FastAPI
from __init__ import api_router

app = FastAPI(title= "Latihan Fast Api Auth", summary= "Endpoint Fast API", version= "1.0")

app.include_router(api_router)