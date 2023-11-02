from logger import Logger
import logging
from multiprocessing import Process

def other_process(logger: Logger):
    logger.configure_emitter()
    local_logger = logger.get_logger('here')
    local_logger.log(logging.INFO, 'log entry')

if __name__ == '__main__':
    # create the object
    logger = Logger()
    logger.start()
    
    p = Process(target=other_process, args=(logger,))
    p.start()
    p.join()
