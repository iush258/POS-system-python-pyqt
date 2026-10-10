from fastapi import FastAPI

from app.api.admin import router as admin_router
from app.api.auth import router as auth_router
from app.api.products import router as products_router
from app.api.categories import router as categories_router
from app.api.inventory import router as inventory_router
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="0.1.0",
)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(products_router)
app.include_router(categories_router)
app.include_router(inventory_router)


@app.get("/")
def home() -> dict[str, str]:
    return {
        "message": "WELCOME TO THE POS SYSTEM",
    }

@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
    }