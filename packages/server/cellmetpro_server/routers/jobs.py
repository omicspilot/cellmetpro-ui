from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cellmetpro_server.database import get_session
from cellmetpro_server.models import Job, Project
from cellmetpro_server.schemas import JobCreate, JobResponse
from cellmetpro_server.utils.const import ErrCode

router = APIRouter(prefix="/projects", tags=["Jobs", "Projects"])

Session = Annotated[AsyncSession, Depends(get_session)]


@router.get("/{project_id}/jobs", response_model=list[JobResponse])
async def list_jobs(project_id: str, session: Session) -> list[Job]:
    project = await session.get(Project, project_id)
    if project is None or project.deleted_at is not None:
        raise HTTPException(status_code=404, detail=ErrCode.PROJECT_NOT_FOUND)

    jobs = await session.scalars(select(Job).where(Job.project_id == project_id))

    return list(jobs.all())


@router.get("/{project_id}/jobs/{job_id}", response_model=JobResponse)
async def get_job(project_id: str, job_id: str, session: Session) -> Job:
    project = await session.get(Project, project_id)
    if project is None or project.deleted_at is not None:
        raise HTTPException(status_code=404, detail=ErrCode.PROJECT_NOT_FOUND)

    job = await session.scalar(
        select(Job).where(Job.id == job_id, Job.project_id == project_id)
    )
    if job is None:
        raise HTTPException(status_code=404, detail=ErrCode.JOB_NOT_FOUND)

    return job


@router.post("/{project_id}/jobs", response_model=JobResponse)
async def create_job(project_id: str, body: JobCreate, session: Session) -> Job:
    project = await session.get(Project, project_id)
    if project is None or project.deleted_at is not None:
        raise HTTPException(status_code=404, detail=ErrCode.PROJECT_NOT_FOUND)

    job_id = str(uuid4())
    job = Job(id=job_id, project_id=project_id, analysis_type=body.analysis_type)

    session.add(job)
    await session.commit()
    await session.refresh(job)

    return job
