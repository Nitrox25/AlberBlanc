import pytest
import asyncio
import websockets
import subprocess


@pytest.fixture(scope="session", autouse=True)
def run_websocket_api():
    """
    фикстура для запуска ./tester.so .
    """
    process = subprocess.Popen(["./tester.so", "127.0.0.1", "4000"])
    yield
    process.kill()

@pytest.fixture(scope="function")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def websocket_connection():
    uri = "ws://127.0.0.1:4000"
    try:
        async with websockets.connect(uri) as ws:
            yield ws
    except websockets.exceptions.ConnectionClosedError as e:
        # Обработка ошибки
        print(f"Connection closed with code {e.code}: {e.reason}")
    except Exception as e:
        # Обработка других исключений
        print(f"Unexpected error: {e}")
