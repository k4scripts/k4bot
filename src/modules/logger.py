import os
import logging

LOGGING_LEVEL = int(os.getenv('LOGGING_LEVEL', 2)) * 10

modules = ['discord', 'httpx',]
for module in modules:
    logging.getLogger(module).setLevel((LOGGING_LEVEL + 10) if LOGGING_LEVEL < 50 else 50)

logging.basicConfig(level=LOGGING_LEVEL, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger('k4bot')
