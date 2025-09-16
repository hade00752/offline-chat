import asyncio
import argparse
import yaml
from . import discovery, routing, dtn, transport, message

import uuid

class MeshNode:
    def __init__(self, config):
        self.config = config
        self.node_id = str(uuid.uuid4())  # stable unique ID
        self.peers = {}
        self.queue = dtn.DTNQueue()
        self.router = routing.Router(self)

    async def start(self):
        print(f"[*] Starting mesh node on port {self.config['port']}...")
        await discovery.start_discovery(self)
        asyncio.create_task(transport.listen(self))
        asyncio.create_task(self.control_server())

        # Keep running forever
        await asyncio.Future()


    async def send_message(self, dest, payload):
        msg = message.build(self, dest, payload)
        await transport.send(self, dest, msg)

    async def control_server(self):
        server = await asyncio.start_server(self.handle_client, "127.0.0.1", self.config["control_port"])
        print(f"[*] Control API listening on {self.config['control_port']}")
        async with server:
            await server.serve_forever()

    async def handle_client(self, reader, writer):
        data = await reader.read(1024)
        text = data.decode().strip()

        if text.startswith("BROADCAST "):
            payload = text[len("BROADCAST "):]
            print(f"[*] Broadcasting: {payload} to {len(self.peers)} peers")
            for peer_id, (ip, port)  in self.peers.items():
                msg = message.build(self, peer_id, payload)
                await transport.send(self, peer_id, msg)
        elif " " in text:
            dest, payload = text.split(" ", 1)
            await self.send_message(dest, payload)

        writer.close()



    async def control_server(self):
        try:
            server = await asyncio.start_server(
                self.handle_client,
                "127.0.0.1",
                self.config["control_port"]
            )
            print(f"[*] Control API listening on {self.config['control_port']}")
            async with server:
                await server.serve_forever()
        except Exception as e:
            print(f"[ERROR] Control server failed: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/default.yaml")
    args = parser.parse_args()

    cfg = yaml.safe_load(open(args.config))
    node = MeshNode(cfg)
    asyncio.run(node.start())

if __name__ == "__main__":
    main()
