import asyncio
import socket
import json

BROADCAST_PORT = 50000

async def start_discovery(node):
    loop = asyncio.get_event_loop()
    loop.create_task(listen_for_beacons(node))
    loop.create_task(send_beacons(node))

async def send_beacons(node):
    # Create a UDP socket for sending
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        beacon = {"id": node.node_id, "port": node.config["port"]}
        sock.sendto(json.dumps(beacon).encode(), ('<broadcast>', BROADCAST_PORT))
        await asyncio.sleep(node.config.get("beacon_interval", 5))

async def listen_for_beacons(node):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", BROADCAST_PORT))

    loop = asyncio.get_event_loop()
    while True:
        data, addr = await loop.run_in_executor(None, sock.recvfrom, 1024)
        beacon = json.loads(data.decode())
        if beacon["id"] != node.node_id:  # ignore self
            node.peers[beacon["id"]] = (addr[0], beacon["port"])
            print(f"[DISCOVERY] Found peer {beacon['id']} at {addr[0]}:{beacon['port']}")
