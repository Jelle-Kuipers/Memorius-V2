import logging
import os
from dotenv import load_dotenv

load_dotenv()
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "DEBUG").upper()
LOG_PATH = os.getenv("DATABASE_LOG_PATH", "logs/app.log")

logging.basicConfig(
    filename=LOG_PATH,
    level=getattr(logging, LOGGING_LEVEL, logging.ERROR),
    format='[%(asctime)s] [%(levelname)s] [%(pathname)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%y %H:%M:%S'
)
