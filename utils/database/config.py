import sqlite3
import os
from dotenv import load_dotenv
import logging

# Init logging and ENV variables.
load_dotenv()
DATABASE_PATH = os.getenv("DATABASE_PATH", "databases/database.db")
DATABASE_LOG_PATH = os.getenv("DATABASE_LOG_PATH", "logs/database.log")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "ERROR").upper()

logging.basicConfig(
    filename=DATABASE_LOG_PATH,
    level=getattr(logging, LOGGING_LEVEL, logging.ERROR),
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%d-%m-%y %H:%M:%S'
)
