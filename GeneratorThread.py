import threading
import time

from Dependencies.CreatureManager import CreatureManager


class GeneratorThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.threads = []
        self.lock = threading.Lock()

    def run(self):
        cm = CreatureManager()

        while True:
            cm.db.remove_old_creatures()

            locations = []
            self.lock.acquire()
            for i in reversed(range(len(self.threads))):
                if self.threads[i].keepAlive:
                    if self.threads[i].last_location != (None, None):
                        locations.append(self.threads[i].last_location)
                else:
                    self.threads.pop(i)
            self.lock.release()
            print(locations)
            cm.gen_new_creatures(locations)

            time.sleep(30)

