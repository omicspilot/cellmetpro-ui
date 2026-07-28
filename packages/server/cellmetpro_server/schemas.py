from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from .models import AnalysisType, FileType


class _Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ------- file ------- #


class FileRegister(BaseModel):
    path: str
    file_type: str = FileType.UNSPECIFIED.value


class FileResponse(_Base):
    id: str
    project_id: str
    filename: str
    file_type: str
    status: str
    job_id: str | None
    size_bytes: int
    created_at: datetime


class FileUpdate(BaseModel):
    file_type: str | None = None
    filename: str | None = None


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


# ------- Project ------- #
class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    workspace_path: str | None = None


class ProjectResponse(_Base):
    id: str
    name: str
    description: str | None
    workspace_path: str | None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None
