import os
import logging

LOGGING_LEVEL = int(os.getenv('LOGGING_LEVEL', 2)) * 10

logging.basicConfig(level=LOGGING_LEVEL, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger('k4bot')
