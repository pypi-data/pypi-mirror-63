from threading import Event, Thread

from .engine import Engine
from .timer import TimerEntrypoint


DEFAULT_EXTENSIONS = [TimerEntrypoint]


class Macaw:
    def __init__(self, name):
        self.name = name
        self.running = Event()
        self.engine = Engine({})
        self.extensions = {}

        self.setup()

    def setup(self):
        for extension_cls in DEFAULT_EXTENSIONS:
            extension_cls(self)

    def start(self):
        for extension_name, extension_instance in self.extensions.items():
            self.engine.spawn_thread(extension_instance.start)

        self.running.wait()

    def stop(self):
        for extension_name, extension_instance in self.extensions.items():
            extension_instance.stop()

        self.engine.shutdown()

        self.running.set()

    def run(self):
        try:
            self.start()
        except KeyboardInterrupt:
            self.stop()

    def register_extension(self, extension):
        extension_name = extension.name
        self.extensions[extension_name] = extension

    def dispatch_entrypoint(self):
        print("hi")