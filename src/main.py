"""Entry path."""

from fastapi import FastAPI

from src import application

# from src.auth.router import login_router
from src.config import settings

# from src.users.router import user_router
from src.utils.serializers import MsgSpecJSONResponse

# Adjust the application
# -------------------------------
app: FastAPI = application.create(
    title=settings.PROJECT_NAME,
    openapi_url=settings.OPENAPI_URL,
    docs_url=settings.DOCS_URL,
    debug=settings.DEBUG,
    version=settings.PROJECT_VERSION,
    default_response_class=MsgSpecJSONResponse,
    startup_tasks=[],
    shutdown_tasks=[],
)

# app.include_router(login_router, tags=["Auth"])

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run("src.main:app", port=8001, log_level="debug", reload=True)
