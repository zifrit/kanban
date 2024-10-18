import uvicorn
from fastapi import FastAPI
from src.api import auth, board, user, column
from src.core.logger import LOGGING
from src.core.settings import settings

app = FastAPI(
    title=settings.PROJECT_TITLE,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)

app.include_router(user.router, prefix="/api/users", tags=["user"])
app.include_router(board.router, prefix="/api/board", tags=["board"])
app.include_router(column.router, prefix="/api/column", tags=["column"])
app.include_router(auth.router, prefix="/jwt", tags=["auth"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        log_config=LOGGING,
    )
