import asyncio
import websockets

clients = set()

async def handler(ws, path):
    clients.add(ws)
    async for msg in ws:
        for c in clients:
            if c != ws:
                await c.send(msg)

async def start_api():
    async with websockets.serve(handler, "localhost", 9000):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(start_api())
