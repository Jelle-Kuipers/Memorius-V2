import sqlite3
import logging
from utils.database.config import DATABASE_PATH

# Database connection
def get_connection():
    try:
        return sqlite3.connect(DATABASE_PATH)
    except Exception as e:
        logging.error(f"Database error: {e}")
        raise