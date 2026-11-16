from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import predictions, auth
from contextlib import asynccontextmanager
from app.services.ml_service import load_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = load_model()
    yield
    pass

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predictions.router)
app.include_router(auth.router)