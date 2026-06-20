"""
main.py — FastAPI application entry point
===========================================
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import init_db
from app.api.v1 import simulations, monitors, playbooks, templates, organizations
from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting CrisisSim backend...")
    await init_db()
    logger.info("Database initialized.")
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title="CrisisSim",
    description="Multi-agent crisis simulation engine",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(organizations.router, prefix="/api/v1", tags=["organizations"])
app.include_router(simulations.router, prefix="/api/v1", tags=["simulations"])
app.include_router(monitors.router, prefix="/api/v1", tags=["monitors"])
app.include_router(playbooks.router, prefix="/api/v1", tags=["playbooks"])
app.include_router(templates.router, prefix="/api/v1", tags=["templates"])


@app.get("/")
async def root():
    return {
        "name": "CrisisSim",
        "version": "1.0.0",
        "description": "Multi-agent crisis simulation engine",
        "status": "operational",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
