import uvicorn
from fastapi import FastAPI
from src.api.user import router as user_router
from src.core.logger import LOGGING

app = FastAPI()

app.include_router(user_router, prefix="/user")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        log_config=LOGGING,
    )
