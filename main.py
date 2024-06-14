from contextlib import asynccontextmanager

from fastapi import FastAPI

import uvicorn

from core.config import settings
from api_v1 import router as router_v1
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Allows all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
    )

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
