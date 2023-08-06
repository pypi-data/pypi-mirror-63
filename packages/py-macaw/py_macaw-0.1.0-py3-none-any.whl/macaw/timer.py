from threading import Event
from threading import Thread
from types import SimpleNamespace


class TimerEntrypoint:
    def __init__(self, app):
        self.name = "timer_entrypoint"
        self.app = app
        self.instance_decorators = set()
        self.workers = {}

        if app is not None:
            self.setup(app)

    def setup(self, app):
        app.register_extension(self)
        setattr(app, "timer", self.decorator)

    def start(self):
        for instance in self.instance_decorators:
            thread = Thread(target=instance.run, daemon=True)
            thread.start()
            self.workers[instance] = thread

    def stop(self):
        for instance in self.instance_decorators:
            instance.stop()
            self.workers[instance].join()

    def decorator(self, interval, context=None):
        context = context or {}

        def inner(fn):
            instance = Timer(interval, context, fn)
            self.instance_decorators.add(instance)
            return fn

        return inner


class Timer:
    def __init__(self, interval, context, method):
        self.interval = interval
        self.name = method.__name__
        self.method = method
        self.should_end = Event()
        self.context = SimpleNamespace(**context)

    def stop(self):
        self.should_end.set()

    def run(self):
        while True:
            if self.should_end.is_set():
                break

            self.should_end.wait(self.interval)

            result = self.method(self.context)
