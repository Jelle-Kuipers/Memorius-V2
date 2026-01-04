import logging
import sys
from utils.database.connection import get_connection

# Event table initialization
def init_db():
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id TEXT NOT NULL,
                    channel_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    event_name TEXT NOT NULL CHECK(length(event_name) <= 50),
                    event_date DATETIME NOT NULL,
                    event_location TEXT NOT NULL CHECK(length(event_location) <= 50),
                    edited_reason TEXT DEFAULT NULL CHECK(length(edited_reason) <= 140),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    edited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    edited_by TEXT DEFAULT NULL,
                    cancelled BOOLEAN DEFAULT 0,
                    cancelled_at TIMESTAMP DEFAULT NULL,
                    cancelled_by TEXT DEFAULT NULL
                )
            ''')
            conn.commit()
            logging.debug("Successfully created the events table.")
    except Exception as e:
        logging.critical(f"Database table init error: {e}")
        sys.exit(1)