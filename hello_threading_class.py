import threading
import time


class Destination:
    def __init__(self):
        self.active = True

    def run(self, name, config):
        while self.active:
            print("in thread", name, config)
            time.sleep(0.5)


destination = Destination()
thread = threading.Thread(target=destination.run, args=("foo", "bar"))
thread.start()
