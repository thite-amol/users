from fastapi import APIRouter, FastAPI

from src import application
from src.auth.router import login_router
from src.config import settings
from src.users.router import user_router

api_router = APIRouter()


@api_router.get("/", status_code=200)
async def root() -> dict:
    """Root Get."""
    return {"msg": "Hello, World!"}


# Adjust the application
# -------------------------------
app: FastAPI = application.create(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
    debug=settings.DEBUG,
    # rest_routers=(rest.products.router, rest.orders.router),
    rest_routers=[user_router],
    startup_tasks=[],
    shutdown_tasks=[],
)

app.include_router(login_router, tags=["Auth"])

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run("src.main:app", port=8001, log_level="debug", reload=True)
