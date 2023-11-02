import logging
import logging.handlers
from multiprocessing import Process, Queue, Event
from queue import Empty

class Logger(Process):
    '''
    Simple multiprocessing logger class to handle logging from multiple processes to the same 
    log file using a multiprocessing Queue. 
    The logger objects needs to be handed to each process that wants to log to the file.
    '''

    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    def __init__(
            self, 
            filename: str = 'log.txt', 
            listener_level = logging.DEBUG, 
            *args, **kwargs
        ) -> None:
        
        super().__init__(*args, **kwargs)
        
        self.filename = filename
        self.queue = Queue()
        self.stop_evt = Event()
        self.listener_level = listener_level

    def configure_listener(self) -> None:
        '''
        Configure root logger for the listener process
        '''
        root = logging.getLogger()
        root.setLevel(self.listener_level)
        handler = logging.FileHandler(self.filename, 'w')
        formatter = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        handler.setLevel(self.listener_level)
        root.addHandler(handler)
        
    def configure_emitter(self, level = logging.DEBUG) -> None:
        '''
        Configure root logger for the emitter process, this needs to be called
        at the beginning of each emitter process
        '''
        handler = logging.handlers.QueueHandler(self.queue)
        handler.setLevel(level)
        root = logging.getLogger()
        root.addHandler(handler)
        root.setLevel(level)

    def get_logger(self, name: str) -> logging.Logger:
        '''
        Returns logger with a specific name
        '''
        return logging.getLogger(name)

    def run(self) -> None:
        '''
        Listener runs in its own process
        '''

        self.configure_listener()
        while not self.stop_evt.is_set():
            try:
                record = self.queue.get_nowait()
                if record is None:
                    break
                logger = logging.getLogger(record.name)
                logger.handle(record)
            except Empty: # should I sleep to avoid CPU usage ?
                pass

    def stop(self) -> None:
        '''
        Stops listener
        '''
        self.stop_evt.set()