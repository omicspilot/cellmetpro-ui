import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from cellmetpro_server.utils.jobs import JobStatus, job_store

router = APIRouter(prefix="/ws", tags=["WebSocket"])

POLL_INTERVAL = 0.5


@router.websocket("/jobs/{job_id}")
async def stream_job_progress(job_id: str, websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            job = job_store.get(job_id)
            if job is None:
                await websocket.send_json({"error": "job not found"})
                await websocket.close(1008)
                return

            await websocket.send_json(job.model_dump(mode="json"))

            if job.status in (JobStatus.COMPLETE, JobStatus.FAILED):
                await websocket.close(1000)
                return

            await asyncio.sleep(POLL_INTERVAL)

    except WebSocketDisconnect:
        pass
