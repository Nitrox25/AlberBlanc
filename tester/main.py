import websockets
import asyncio
import json
import sys


async def do_smth():
    uri = "ws://127.0.0.1:4000"
    async with websockets.connect(uri) as ws:
        await ws.send('{"id": "83ec36df-d68b-4fbd-9f89-4c1f53d80562", "method": "select"}')
        repl = await ws.recv()
        print(json.loads(repl))


asyncio.get_event_loop().run_until_complete(do_smth())

