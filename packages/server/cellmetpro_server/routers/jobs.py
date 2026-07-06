from fastapi import APIRouter, HTTPException

from cellmetpro_server.jobs import Job, job_store

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/", response_model=list[Job])
async def list_jobs() -> list[Job]:
    return job_store.list()


@router.get("/{job_id}", response_model=Job)
async def get_job(job_id: str) -> Job:
    job = job_store.get(job_id)
    if job is None:
        raise HTTPException(404)
    return job
