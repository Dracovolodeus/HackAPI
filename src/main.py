from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
from fastapi import FastAPI

from api import router as api_router
from core.config import settings

from database import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield  # Start
    await db_helper.dispose()  # Shutdown


main_app = FastAPI(
    lifespan=lifespan,
)

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
main_app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
