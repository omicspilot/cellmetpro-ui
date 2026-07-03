import httpx

from cellmetpro_server import __version__


async def test_health(client: httpx.AsyncClient) -> None:
    response = await client.get("/api/v1/system/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_version(client: httpx.AsyncClient) -> None:
    response = await client.get("/api/v1/system/version")
    assert response.status_code == 200
    assert response.json() == {"server": __version__, "cellmetpro": "not installed"}
