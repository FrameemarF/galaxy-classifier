from fastapi import FastAPI
from app.routers.predictions import router
from contextlib import asynccontextmanager
from app.services.ml_service import load_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = load_model()
    yield
    pass

app = FastAPI(lifespan=lifespan)

app.include_router(router)