class Router:
    def __init__(self, node):
        self.node = node

    def next_hop(self, dest):
        # For now, naive: if peer known, send direct
        if dest in self.node.peers:
            return self.node.peers[dest]
        return None
