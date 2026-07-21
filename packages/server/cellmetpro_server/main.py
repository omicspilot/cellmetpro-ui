import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from alembic import command
from alembic.config import Config
from fastapi import FastAPI

from cellmetpro_server import __version__

from .config import get_settings
from .database import engine
from .routers import io, jobs, system, ws


def _run_migrations() -> None:
    alembic_ini_path = Path(__file__).parent.parent / "alembic.ini"
    cfg = Config(str(alembic_ini_path))
    command.upgrade(cfg, "head")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    Path.home().joinpath(".cellmetpro").mkdir(parents=True, exist_ok=True)
    await asyncio.to_thread(_run_migrations)
    yield
    await engine.dispose()


app = FastAPI(
    title="CellMetPro Server",
    version=__version__,
    description="Cellular Metabolic Profiler",
    lifespan=lifespan,
)
app.include_router(system.router, prefix="/api/v1")
app.include_router(io.router, prefix="/api/v1")
app.include_router(jobs.router, prefix="/api/v1")
app.include_router(ws.router, prefix="/api/v1")


def run() -> None:
    settings = get_settings()
    uvicorn.run(
        "cellmetpro_server.main:app",
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level,
        reload=settings.reload,
    )
