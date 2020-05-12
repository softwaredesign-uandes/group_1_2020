class Publisher:
    def __init__(self):
        self.subscribers = []

    def add_subscriber(self, subscriber):
        self.subscribers.append(subscriber)

    def notify(self, event):
        for s in self.subscribers:
            s.handle(event)
