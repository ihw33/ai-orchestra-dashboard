import asyncio
import websockets
import json

async def listen():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print(json.dumps(data, indent=2))

if __name__ == "__main__":
    asyncio.run(listen())
