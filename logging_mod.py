import logging
import sys

# logging
def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler('log.txt', mode='a')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    lg = logging.getLogger(name)
    lg.setLevel(logging.DEBUG)
    lg.addHandler(handler)
    lg.addHandler(screen_handler)
    return lg
#lg = setup_custom_logger("autorecorder")