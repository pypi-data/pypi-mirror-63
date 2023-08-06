from threading import Event, Thread
from concurrent.futures import ThreadPoolExecutor

class Engine:
    def __init__(self, config):
        self.threads = []
        self.futures = []
        self.pool = ThreadPoolExecutor(max_workers=10)

    def spawn_thread(self, fn, daemon=True):
        thread = Thread(target=fn, daemon=daemon)
        thread.start()
        self.threads.append(thread)

    def submit(self, fn, *args, **kwargs):
        future = self.pool.submit(fn, *args, **kwargs)
        self.futures.append(future)

    def shutdown(self):
        for future in self.futures:
            future.cancel()
        self.pool.shutdown(wait=True)

        for thread in self.threads:
            thread.join()
