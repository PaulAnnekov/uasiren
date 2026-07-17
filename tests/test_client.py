import asyncio

import pytest
from aiohttp import ClientSession, web
from aiohttp.test_utils import TestServer

from uasiren.client import Client


async def _make_server(delay):
    async def handler(request):
        await asyncio.sleep(delay)
        return web.json_response([{"activeAlerts": []}])

    app = web.Application()
    app.router.add_get("/alerts/1", handler)
    server = TestServer(app)
    await server.start_server()
    return server


async def test_default_timeout_is_30():
    assert Client.REQUEST_TIMEOUT == 30


async def test_custom_timeout_times_out_on_slow_response(monkeypatch):
    server = await _make_server(delay=0.5)
    try:
        monkeypatch.setattr(Client, "BASE_PATH", str(server.make_url("")).rstrip("/"))
        async with ClientSession() as session:
            client = Client(session, timeout=0.1)
            with pytest.raises(asyncio.TimeoutError):
                await client.get_alerts("1")
    finally:
        await server.close()


async def test_custom_timeout_allows_slow_response(monkeypatch):
    server = await _make_server(delay=0.3)
    try:
        monkeypatch.setattr(Client, "BASE_PATH", str(server.make_url("")).rstrip("/"))
        async with ClientSession() as session:
            client = Client(session, timeout=5)
            result = await client.get_alerts("1")
            assert result == [{"activeAlerts": []}]
    finally:
        await server.close()


async def test_timeout_defaults_when_not_passed(monkeypatch):
    server = await _make_server(delay=0)
    try:
        monkeypatch.setattr(Client, "BASE_PATH", str(server.make_url("")).rstrip("/"))
        async with ClientSession() as session:
            client = Client(session)
            result = await client.get_alerts("1")
            assert result == [{"activeAlerts": []}]
    finally:
        await server.close()
