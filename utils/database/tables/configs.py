import logging
import sys
from utils.database.connection import get_connection

# New table initialization
def init_db():
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS server_configs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id TEXT NOT NULL,
                    default_event_channel TEXT DEFAULT NULL,
                    default_event_name TEXT DEFAULT 'New Event',
                    default_event_location TEXT DEFAULT 'To be determined',
                    enable_automatic_polling BOOLEAN DEFAULT 0,
                    default_polling_time TIME DEFAULT '20:00:00'
                )
            ''')
            conn.commit()
            logging.debug("Successfully created the server_configs table.")
    except Exception as e:
        logging.critical(f"Database tabel init error: {e}")
        sys.exit(1)