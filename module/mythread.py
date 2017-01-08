import threading
import time


class MyThread (threading.Thread):
    def __init__(self, name, func):
        threading.Thread.__init__(self)
        self.name = name
        self.exitThreadFlag = 0
        self.func = func

    def run(self):
        print("Starting loop thread:", self.name)

        while self.exitThreadFlag < 1:
            self.func()
            time.sleep(0.5)

        print("Stop loop thread:", self.name)
