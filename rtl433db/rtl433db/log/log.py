import logging

log_format = '%(asctime)s.%(msecs)d|%(levelname)s\
|%(module)s.%(funcName)s:%(lineno)d %(message)s'

logging.basicConfig(level=logging.INFO,
                    format=log_format,
                    datefmt='%Y-%m-%d %H:%M:%S')
