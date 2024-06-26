from multiprocessing_logger.logger import Logger
from multiprocessing import Process

def add_info_entry(logger: Logger):
    logger.configure_emitter()
    local_logger = logger.get_logger('here')
    local_logger.info('log entry')

def add_debug_entry(logger: Logger):
    logger.configure_emitter()
    local_logger = logger.get_logger('there')
    local_logger.debug('other log entry')

def add_warning_entry(logger: Logger):
    logger.configure_emitter()
    local_logger = logger.get_logger('now')
    local_logger.warning('yet another log entry')

if __name__ == '__main__':


    logger = Logger()
    logger.start()

    logger2 = Logger(
        'log2.txt', 
        listener_level=Logger.WARNING,
        format_str='%(levelname)-8s %(asctime)s %(name)s %(message)s'
    )
    logger2.start()

    # -------------------------------------------------------
    
    p = Process(target=add_info_entry, args=(logger,))
    p0 = Process(target=add_debug_entry, args=(logger,))
    p1 = Process(target=add_warning_entry, args=(logger2,))
    p1.start()
    p0.start()
    p.start()
    p.join()
    p0.join()
    p1.join()

    # -------------------------------------------------------

    p = Process(target=add_info_entry, args=(logger2,))
    p0 = Process(target=add_debug_entry, args=(logger2,))
    p1 = Process(target=add_warning_entry, args=(logger,))
    p1.start()
    p0.start()
    p.start()
    p.join()
    p0.join()
    p1.join()

    logger2.stop()
    logger.stop()

