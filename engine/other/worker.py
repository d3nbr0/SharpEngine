from threading import Thread
from time import sleep
import engine.other.hooks as hooks


class Worker:
    def __init__(self):
        self.enabled = True
        self.is_busy = False
        self.update = None
        self.thread = Thread(target=self.pool)
        self.thread.start()

    def pool(self):
        while self.enabled:
            if self.update is not None:
                self.is_busy = True
                hooks.do(self.update['type'], self.update['object'])
                self.update = None
                self.is_busy = False
            sleep(0.01)
