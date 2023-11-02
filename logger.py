import logging
import logging.handlers
from multiprocessing import Process, Queue, Event

class Logger(Process):
    def __init__(self, filename: str = 'log.txt', *args, **kwargs):
        super.__init__(*args, **kwargs)
        self.filename = filename
        self.queue = Queue()
        self.stop_evt = Event()

    def configure_listener(self) -> None:
        '''
        Configure root logger for the listener process
        '''
        root = logging.getLogger()
        handler = logging.handlers.FileHandler(self.filename, 'a')
        formatter = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(formatter)

    def configure_emitter(self, level = logging.DEBUG) -> None:
        '''
        Configure root logger for the emitter process
        '''
        handler = logging.handlers.QueueHandler(self.queue)
        root = logging.getLogger()
        root.addHandler(handler)
        root.setLevel(level)

    def get_logger(self, name: str) -> logging.Logger:
        return logging.getLogger(name)

    def run(self):
        self.configure_listener()
        while not self.stop_evt.is_set():
            record = self.queue.get()
            if record is None:
                break
            logger = logging.getLogger(record.name)
            logger.handle(record)

    def stop(self):
        self.stop_evt.set()