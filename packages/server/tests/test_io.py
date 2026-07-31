import uuid

import httpx


async def test_upload_valid_file(client: httpx.AsyncClient) -> None:
    response = await client.post(
        "/api/v1/files/upload",
        files={"file": ("matrix.h5ad", b"fake content", "application/octet-stream")},
    )
    assert response.status_code == 200
    data = response.json()
    assert "file_id" in data
    assert data["filename"] == "matrix.h5ad"
    assert data["size_bytes"] > 0


async def test_upload_invalid_extension(client: httpx.AsyncClient) -> None:
    response = await client.post(
        "/api/v1/files/upload",
        files={"file": ("malware.exe", b"bad content", "application/octet-stream")},
    )
    assert response.status_code == 422


async def test_get_existing_file(client: httpx.AsyncClient) -> None:
    # first upload
    upload = await client.post(
        "/api/v1/files/upload",
        files={"file": ("counts.csv", b"gene,cell\n1,2", "text/csv")},
    )
    file_id = upload.json()["file_id"]

    # then fetch
    response = await client.get(f"/api/v1/files/{file_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["file_id"] == file_id
    assert data["filename"] == "counts.csv"


async def test_get_nonexistent_file(client: httpx.AsyncClient) -> None:
    fake_id = str(uuid.uuid4())
    response = await client.get(f"/api/v1/files/{fake_id}")
    assert response.status_code == 404


async def test_delete_file(client: httpx.AsyncClient) -> None:
    # upload
    upload = await client.post(
        "/api/v1/files/upload",
        files={"file": ("sparse.mtx", b"%%MatrixMarket", "text/plain")},
    )
    file_id = upload.json()["file_id"]

    # delete
    delete_response = await client.delete(f"/api/v1/files/{file_id}")
    assert delete_response.status_code == 204

    # confirm gone
    get_response = await client.get(f"/api/v1/files/{file_id}")
    assert get_response.status_code == 404
