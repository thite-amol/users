from fastapi import APIRouter, FastAPI

from src.auth.router import login_router
from src.config import settings

api_router = APIRouter()


def start_application():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"/openapi.json",
    )
    return app


app = start_application()


@api_router.get("/", status_code=200)
def root() -> dict:
    """
    Root Get
    """
    return {"msg": "Hello, World!"}


app.include_router(api_router)
app.include_router(login_router, tags=["login"])

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run("src.main:app", port=8001, log_level="debug", reload=True)
