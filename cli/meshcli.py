import click
import socket

@click.group()
def cli():
    pass

@cli.command()
@click.argument("node")
@click.argument("msg")
def broadcast(node, msg):
    """
    Broadcast a message from NODE to all known peers.
    Example: python3 -m cli.meshcli broadcast A "hello everyone"
    """
    control_ports = {"A": 6001, "B": 6002, "C": 6003}
    port = control_ports[node]

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", port))
    sock.sendall(f"BROADCAST {msg}".encode())
    sock.close()
    print(f"[*] Broadcast from Node {node}: {msg}")


@cli.command()
def peers():
    print("[*] (TODO) Query peers from API")

@cli.command()
@click.argument("node")
@click.argument("dest")
@click.argument("msg")
def send(node, dest, msg):
    """
    Send message from NODE (A, B, or C) to DEST peer ID.
    Example: python3 -m cli.meshcli send A 12345 "hello"
    """
    control_ports = {"A": 6001, "B": 6002, "C": 6003}
    port = control_ports[node]

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", port))
    sock.sendall(f"{dest} {msg}".encode())
    sock.close()
    print(f"[*] Sent from Node {node} -> {dest}: {msg}")

if __name__ == "__main__":
    cli()
