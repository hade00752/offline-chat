import asyncio
import websockets

async def chat():
    uri = "ws://localhost:9000"
    async with websockets.connect(uri) as ws:
        while True:
            msg = input("You: ")
            await ws.send(msg)
            reply = await ws.recv()
            print(f"[Chat] {reply}")

if __name__ == "__main__":
    asyncio.run(chat())
