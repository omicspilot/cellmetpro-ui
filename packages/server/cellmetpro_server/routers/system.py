from fastapi import APIRouter
from pydantic import BaseModel

from cellmetpro_server import __version__

router = APIRouter(prefix="/system", tags=["System"])


class HealthResponse(BaseModel):
    status: str


class VersionResponse(BaseModel):
    server: str
    cellmetpro: str


@router.get("/health", response_model=HealthResponse)
async def check_health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/version", response_model=VersionResponse)
async def get_version() -> VersionResponse:
    return VersionResponse(server=__version__, cellmetpro="not installed")
