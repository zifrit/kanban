import uvicorn
from fastapi import FastAPI
from src.api.user import router as user_router
from src.api import auth
from src.core.logger import LOGGING
from src.core.settings import settings

app = FastAPI(
    title=settings.PROJECT_TITLE,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)

app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        log_config=LOGGING,
    )
