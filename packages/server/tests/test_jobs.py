import uuid

import httpx

from cellmetpro_server.jobs import JobStatus, job_store


async def test_get_existing_job(client: httpx.AsyncClient) -> None:
    job = job_store.create()

    response = await client.get(f"/api/v1/jobs/{job.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == job.id
    assert data["status"] == JobStatus.PENDING.value


async def test_get_nonexistant_job(client: httpx.AsyncClient) -> None:
    response = await client.get(f"/api/v1/jobs/{uuid.uuid4()}")
    assert response.status_code == 404


async def test_list_jobs(client: httpx.AsyncClient) -> None:
    job = job_store.create()

    response = await client.get("/api/v1/jobs/")
    assert response.status_code == 200
    job_ids = [j["id"] for j in response.json()]
    assert job.id in job_ids


async def test_job_status_transitions(client: httpx.AsyncClient) -> None:
    job = job_store.create()
    assert job.status == JobStatus.PENDING

    await job_store.update(
        job.id, status=JobStatus.RUNNING, step="Computing", progress=30
    )
    response = await client.get(f"/api/v1/jobs/{job.id}")
    data = response.json()
    assert data["status"] == JobStatus.RUNNING
    assert data["progress"] == 30
    assert data["step"] == "Computing"

    await job_store.update(job.id, status=JobStatus.COMPLETE, progress=100)
    response = await client.get(f"/api/v1/jobs/{job.id}")
    assert response.json()["status"] == JobStatus.COMPLETE


async def test_update_nonexisting_job() -> None:
    job = await job_store.update(str(uuid.uuid4()))
    assert job is None
