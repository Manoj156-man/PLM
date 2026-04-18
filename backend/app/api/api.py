from fastapi import APIRouter

from app.api.endpoints import auth, products, agents

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
