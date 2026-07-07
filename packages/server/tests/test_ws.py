import uuid

from starlette.testclient import TestClient

from cellmetpro_server.jobs import JobStatus, job_store
from cellmetpro_server.main import app


# Note: Because the WebSocket handler loops until the job is terminal,
# your tests need to put the job into a terminal state before connecting,
# or they will block forever
async def test_ws_streams_completed_job() -> None:
    job = job_store.create()
    await job_store.update(job.id, status=JobStatus.COMPLETE, progress=100)

    messages = []
    with TestClient(app).websocket_connect(f"/api/v1/ws/jobs/{job.id}") as ws:
        while True:
            try:
                messages.append(ws.receive_json())
            except Exception:
                break
    assert len(messages) > 0
    assert messages[-1]["status"] == JobStatus.COMPLETE.value
    assert messages[-1]["progress"] == 100


def test_ws_unknown_job() -> None:
    with TestClient(app).websocket_connect(f"/api/v1/ws/jobs/{uuid.uuid4()}") as ws:
        data = ws.receive_json()
        assert "error" in data
