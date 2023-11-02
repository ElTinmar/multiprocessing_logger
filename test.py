from logger import Logger
import logging
from multiprocessing import Process

def add_info_entry(logger: Logger):
    logger.configure_emitter()
    local_logger = logger.get_logger('here')
    local_logger.info('log entry')

def add_debug_entry(logger: Logger):
    logger.configure_emitter()
    local_logger = logger.get_logger('there')
    local_logger.debug('other log entry')

if __name__ == '__main__':

    # -------------------------------------------------------

    logger = Logger()
    logger.start()
    
    p = Process(target=add_info_entry, args=(logger,))
    p0 = Process(target=add_debug_entry, args=(logger,))
    p0.start()
    p.start()
    p.join()
    p0.join()

    logger.stop()

    # -------------------------------------------------------

    logger2 = Logger('log2.txt', listener_level=logging.WARNING)
    logger2.start()
    
    p = Process(target=add_info_entry, args=(logger2,))
    p0 = Process(target=add_debug_entry, args=(logger2,))
    p0.start()
    p.start()
    p.join()
    p0.join()

    logger2.stop()
