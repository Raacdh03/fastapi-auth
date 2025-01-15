from fastapi import APIRouter
from routes import *

api_router = APIRouter(prefix="/v1")

api_router.include_router(router= appRoute, tags= ["App Router"])
