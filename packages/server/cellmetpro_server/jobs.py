import asyncio
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"


class Job(BaseModel):
    id: str
    status: JobStatus = JobStatus.PENDING
    step: str = ""
    progress: int = 0
    message: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    result: dict[str, Any] | None = None


class JobStore:
    def __init__(self) -> None:
        self._jobs: dict[str, Job] = {}
        self._lock: asyncio.Lock = asyncio.Lock()

    def create(self) -> Job:
        job_id = str(uuid.uuid4())
        job = Job(
            id=job_id,
            step="Uploading file",
            message="new job creation",
        )
        self._jobs[job_id] = job
        return job

    def get(self, job_id: str) -> Job | None:
        return self._jobs.get(job_id)

    def list(self) -> list[Job]:
        return list(self._jobs.values())

    async def update(self, job_id: str, **kwargs: Any) -> Job | None:
        async with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                return None
            updated = job.model_copy(
                update={**kwargs, "updated_at": datetime.now(timezone.utc)}
            )
            self._jobs[job_id] = updated
            return updated


job_store = JobStore()
