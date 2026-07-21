from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from .models import AnalysisType


class _Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ------- Project ------- #
class ProjectCreate(BaseModel):
    name: str
    description: str | None = None


class ProjectResponse(_Base):
    id: str
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime


# ------- file ------- #
class FileResponse(_Base):
    id: str
    project_id: str
    filename: str
    size_bytes: int
    created_at: datetime


# ------- Job ------- #
class JobCreate(BaseModel):
    analysis_type: str = AnalysisType.UNSPECIFIED.value


class JobResponse(_Base):
    id: str
    project_id: str
    analysis_type: str
    status: str
    step: str
    progress: int
    message: str
    results_meta: dict[str, Any] | None
    created_at: datetime
    updated_at: datetime
