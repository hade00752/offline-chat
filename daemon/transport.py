import socket
from . import message
import asyncio
async def listen(node):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("0.0.0.0", node.config["port"]))
    print(f"[*] Listening on {node.config['port']}")

    while True:
        data, addr = await asyncio.get_event_loop().run_in_executor(None, server.recvfrom, 4096)
        try:
            msg = message.parse(data)
            print(f"[MSG] From {msg['src']}: {msg['payload']} (via {addr})")
        except Exception as e:
            print(f"[ERROR] Failed to parse message from {addr}: {e}")

async def send(node, dest, msg):
    if dest in node.peers:
        ip, port = node.peers[dest]
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(msg, (ip, port))
        sock.close()
        print(f"[SEND] Sent message to {dest} at {ip}:{port}")
    else:
        node.queue.store(msg)
        print(f"[DTN] Queued message for {dest}")
