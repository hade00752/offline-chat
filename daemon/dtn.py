class DTNQueue:
    def __init__(self):
        self.queue = []

    def store(self, msg):
        self.queue.append(msg)

    def deliver(self, node):
        delivered = []
        for msg in self.queue:
            if msg["dest"] in node.peers:
                # try to send (placeholder)
                delivered.append(msg)
        # Remove delivered messages
        self.queue = [m for m in self.queue if m not in delivered]
