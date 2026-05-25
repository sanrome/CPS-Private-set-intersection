class MessageBus:
    def __init__(self):
        self.messages = {}

    def send(self, sender, receiver, data):
        if receiver not in self.messages:
            self.messages[receiver] = []

        self.messages[receiver].append((sender, data))

    def receive(self, receiver):
        if receiver not in self.messages:
            return []

        msgs = self.messages[receiver]
        self.messages[receiver] = []

        return msgs