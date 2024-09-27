import uvicorn
from fastapi import FastAPI
from src.utils.logging_setings import LOGGING

app = FastAPI()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        log_config=LOGGING,
    )
