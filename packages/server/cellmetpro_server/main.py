import uvicorn
from fastapi import FastAPI

from cellmetpro_server import __version__

from .config import get_settings
from .routers import io, jobs, system, ws

app = FastAPI(
    title="CellMetPro Server",
    version=__version__,
    description="Cellular Metabolic Profiler",
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
