import sqlite3
import logging
import os
import sys
from dotenv import load_dotenv

# Init logging and ENV variables.
load_dotenv()
DATABASE_PATH = os.getenv("DATABASE_PATH", "databases/database.db")

# Database connection
def get_connection():
    try:
        return sqlite3.connect(DATABASE_PATH)
    except Exception as e:
        logging.critical(f"Database connection: {e}")
        sys.exit(1)