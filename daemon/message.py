import json
import time

def build(node, dest, payload):
    return json.dumps({
        "src": node.node_id,     # use UUID, not id(node)
        "dest": dest,
        "payload": payload,
    }).encode()

def parse(data):
    return json.loads(data.decode())
